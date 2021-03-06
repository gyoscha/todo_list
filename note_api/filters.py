from typing import Optional

from django.db.models import Q
from django_filters import rest_framework as filters

from note.models import Note


class NoteFilter(filters.FilterSet):
    class Meta:
        model = Note
        fields = [
            'important', 'public',
        ]


def note_status_filter(queryset, status: Optional[str]):
    """
    Фильтрация записей по состоянию (status).
    """
    if status is not None:
        return queryset.filter(
            Q(status=status)
        )
    else:
        return queryset


def note_multi_status_filter(queryset, status_1: Optional[str], status_2: Optional[str]):
    """
    Фильтрация записей по нескольким состояниям (status).
    """
    if (status_1 is not None) and (status_2 is not None):
        return queryset.filter(
            Q(status=status_1) | Q(status=status_2)
        )
    elif status_1 is None:
        return note_status_filter(queryset, status_2)
    elif status_2 is None:
        return note_status_filter(queryset, status_1)
    else:
        return queryset


def note_important_filter(queryset, important: Optional[bool]):
    """
    Фильтрация записей по важности (important).
    """
    if important is not None:
        return queryset.filter(important=important)
    else:
        return queryset


def note_public_filter(queryset, public: Optional[bool]):
    """
    Фильтрация записей по публичности (public).
    """
    if public is not None:
        return queryset.filter(public=public)
    else:
        return queryset
