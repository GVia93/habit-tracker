import pytest
from django.urls import reverse

from apps.habits.models import Habit


def _items(data):
    """Универсально достаём список элементов (с пагинацией или без)."""
    return data["results"] if isinstance(data, dict) and "results" in data else data


@pytest.mark.django_db
def test_create_habit_success(api_client, create_user):
    """Успешное создание привычки авторизованным пользователем."""
    user = create_user(email="x@y.com")
    api_client.force_authenticate(user=user)

    url = reverse("habits:habit-list")
    payload = {
        "action": "Пить воду",
        "place": "Кухня",
        "time": "09:00:00",
        "is_pleasant": False,
        "reward": "Кофе",
        "duration_seconds": 60,
        "periodicity": 1,
        "is_public": True,
    }
    r = api_client.post(url, payload, format="json")

    assert r.status_code == 201
    assert Habit.objects.filter(user=user, action="Пить воду").exists()


@pytest.mark.django_db
def test_pleasant_cannot_have_reward(api_client, create_user):
    """Приятная привычка не может иметь награду → 400."""
    user = create_user(email="p@y.com")
    api_client.force_authenticate(user=user)

    url = reverse("habits:habit-list")
    payload = {
        "action": "Шахматы",
        "place": "Дом",
        "time": "20:00:00",
        "is_pleasant": True,
        "reward": "Конфета",
        "duration_seconds": 60,
        "periodicity": 1,
        "is_public": False,
    }
    r = api_client.post(url, payload, format="json")

    assert r.status_code == 400


@pytest.mark.django_db
def test_list_only_own_habits(api_client, create_user):
    """Пользователь видит в /habits/ только свои привычки."""
    u1 = create_user(email="u1@ex.com")
    u2 = create_user(email="u2@ex.com")

    Habit.objects.create(
        user=u1,
        action="Вода",
        place="Кухня",
        time="09:00:00",
        is_pleasant=False,
        reward="Кофе",
        duration_seconds=60,
        periodicity=1,
        is_public=False,
    )
    Habit.objects.create(
        user=u2,
        action="Чтение",
        place="Дом",
        time="21:00:00",
        is_pleasant=True,
        reward="",
        duration_seconds=30,
        periodicity=1,
        is_public=False,
    )

    api_client.force_authenticate(user=u1)
    url = reverse("habits:habit-list")
    r = api_client.get(url)

    assert r.status_code == 200
    items = _items(r.json())
    assert len(items) == 1
    assert items[0]["action"] == "Вода"


@pytest.mark.django_db
def test_public_list_no_auth(api_client, create_user):
    """Публичные привычки доступны без авторизации на /habits/public/."""
    u = create_user(email="pub@ex.com")
    Habit.objects.create(
        user=u,
        action="Пробежка",
        place="Парк",
        time="07:00:00",
        is_pleasant=True,
        reward="",
        duration_seconds=90,
        periodicity=1,
        is_public=True,
    )
    Habit.objects.create(
        user=u,
        action="Медитация",
        place="Дом",
        time="22:00:00",
        is_pleasant=True,
        reward="",
        duration_seconds=60,
        periodicity=1,
        is_public=False,
    )

    url = reverse("habits:habits-public")
    r = api_client.get(url)

    assert r.status_code == 200
    items = _items(r.json())
    assert any(h["action"] == "Пробежка" for h in items)
    assert all(h["action"] != "Медитация" for h in items)


@pytest.mark.django_db
def test_cannot_retrieve_others_habit(api_client, create_user):
    """Нельзя получить чужую привычку по detail → 404 (queryset фильтруется по user)."""
    owner = create_user(email="owner@ex.com")
    other = create_user(email="other@ex.com")

    habit = Habit.objects.create(
        user=owner,
        action="Бассейн",
        place="Клуб",
        time="19:00:00",
        is_pleasant=False,
        reward="Смузи",
        duration_seconds=45,
        periodicity=2,
        is_public=False,
    )

    api_client.force_authenticate(user=other)
    url = reverse("habits:habit-detail", args=[habit.id])
    r = api_client.get(url)

    assert r.status_code in (403, 404)


@pytest.mark.django_db
def test_update_validation(api_client, create_user):
    """PATCH: нельзя сделать is_pleasant=True и одновременно указать reward."""
    user = create_user(email="upd@ex.com")
    api_client.force_authenticate(user=user)

    habit = Habit.objects.create(
        user=user,
        action="Отжимания",
        place="Дом",
        time="08:00:00",
        is_pleasant=False,
        reward="Десерт",
        duration_seconds=60,
        periodicity=1,
        is_public=False,
    )

    url = reverse("habits:habit-detail", args=[habit.id])
    r = api_client.patch(url, {"is_pleasant": True, "reward": "Конфета"}, format="json")

    assert r.status_code == 400
