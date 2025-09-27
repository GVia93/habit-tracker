from rest_framework.pagination import PageNumberPagination


class DefaultPageNumberPagination(PageNumberPagination):
    """Стандартная пагинация по 5 элементов на страницу."""

    page_size = 5
    page_query_param = "page"
