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
        User.objects.create_user(username='test_1', password='1234567')

        Note.objects.create(
            title='TEST_title_1',
            note='TEST_msg_1',
            author_id=1,
            status='AC',
            public=True,
            important=True,
        )
        Note.objects.create(
            title='TEST_title_2',
            note='TEST_msg_2',
            author_id=1,
            status='PO',
            public=False,
            important=True,
        )
        Note.objects.create(
            title='TEST_title_3',
            note='TEST_msg_3',
            author_id=1,
            status='CO',
            public=True,
            important=False
        )
        Note.objects.create(
            title='TEST_title_4',
            note='TEST_msg_4',
            author_id=1,
            status='CO',
            public=True,
            important=True
        )

    def setUp(self) -> None:
        """Перед каждым тестом логиниться"""
        self.client.login(username='test_1', password='1234567')

    def test_filter_by_status(self):
        url = f'/api/v1/notes/?status=AC'

    def test_filter_by_status_multi(self):
        url = f'/api/v1/notes/?status=AC&status=CO'

    def test_filter_by_important(self):
        url = f'/api/v1/notes/?important=False'

    def test_filter_by_public(self):
        url = f'/api/v1/notes/?public=False'

    def test_filter_all(self):
        url = f'/api/v1/notes/?public=True&status=CO&important=True'
