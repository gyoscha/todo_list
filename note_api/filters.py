from typing import Optional


def note_create_at__year_filter(queryset, year: Optional[int]):
    """
    Фильтрация записей по состоянию (status).
    """
    if year is not None:
        return queryset.filter(create_at__year=year)
    else:
        return queryset


def note_update_at__month__gte_filter(queryset, month: Optional[int]):
    """
    Фильтрация записей по важности (important).
    """
    if month is not None:
        return queryset.filter(create_at__month__gte=month)
    else:
        return queryset


def note_create_at__year_filter(queryset, year: Optional[int]):
    """
    Фильтрация записей по публичности (public).
    """
    if year is not None:
        return queryset.filter(create_at__year=year)
    else:
        return queryset
