from django.test import TestCase
from django.contrib.auth.models import User

from note.models import Note
from note_api import filters


class TestNoteFilter(TestCase):
    """
    TESTS:
    1. Фильтрация записей по статусу (один или несколько)
    2. Фильтрация записей по важности
    3. Фильтрация записей по публичности
    4. Применение всех фильтров одновременно
    """
    @classmethod
    def setUpTestData(cls):
        pass

    def test_filter_by_status(self):
        pass

    def test_filter_by_important(self):
        pass

    def test_filter_by_public(self):
        pass
