from __future__ import annotations

import logging
from datetime import timedelta

from celery import shared_task
from django.db.models import Q
from django.utils import timezone

from apps.habits.models import Habit
from apps.integrations.telegram import send_message

logger = logging.getLogger(__name__)


def _time_window_q(now: timezone.datetime, seconds: int = 30) -> Q:
    """
    Возвращает Q-условие для выборки Habit.time в окне [now-Δ; now+Δ],
    где time — поле типа TimeField (возможно пересечение через полночь).
    """
    start = (now - timedelta(seconds=seconds)).time()
    end = (now + timedelta(seconds=seconds)).time()

    if start <= end:
        return Q(time__range=(start, end))
    return Q(time__gte=start) | Q(time__lte=end)


def _passes_periodicity(habit: Habit, now_date) -> bool:
    """
    Проверка периодичности. Если у модели есть created_at/date_start — считаем дни от неё.
    Если нет (или periodicity <= 0) — пропускаем проверку (считаем, что можно отправлять).
    """
    periodicity = getattr(habit, "periodicity", None)
    if not periodicity or periodicity <= 0:
        return True

    base_date = getattr(habit, "created_at", None) or now_date
    try:
        base_date = base_date.date()
    except AttributeError:
        pass

    days = (now_date - base_date).days
    return days % periodicity == 0


@shared_task(bind=True, ignore_result=True)
def send_habit_reminders(self) -> None:
    """
    Каждую минуту ищем привычки, у которых время ~ сейчас (±30с),
    проверяем periodicity и наличие активного Telegram-профиля у пользователя,
    и отправляем напоминание.
    """
    now = timezone.localtime()
    q_time = _time_window_q(now, seconds=30)

    qs = (
        Habit.objects.filter(q_time)
        .select_related("user__telegram_profile")
        .only(
            "id",
            "action",
            "place",
            "time",
            "duration_seconds",
            "periodicity",
            "user__id",
            "user__email",
            "user__telegram_profile__telegram_id",
            "user__telegram_profile__is_active",
        )
    )

    sent = 0
    for habit in qs:
        if not _passes_periodicity(habit, now.date()):
            continue

        tp = getattr(habit.user, "telegram_profile", None)
        if not tp or not getattr(tp, "is_active", False):
            continue

        chat_id = getattr(tp, "telegram_id", None)
        if not chat_id:
            continue

        action = getattr(habit, "action", "Привычка")
        place = getattr(habit, "place", "")
        t_str = getattr(habit, "time", None)
        dur = getattr(habit, "duration_seconds", None)

        parts = [f"⏰ Напоминание: {action}"]
        if place:
            parts.append(f"Место: {place}")
        if t_str:
            parts.append(f"Время: {t_str}")
        if dur:
            parts.append(f"Длительность: {dur} сек")
        text = "\n".join(parts)

        ok = send_message(chat_id=chat_id, text=text)
        if ok:
            sent += 1
        else:
            logger.warning("Не удалось отправить напоминание (habit_id=%s, chat_id=%s)", habit.id, chat_id)

    if sent:
        logger.info("Отправлено напоминаний: %s", sent)
