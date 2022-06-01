from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from note.models import Note, Comment


class TestNoteListCreateAPIView(APITestCase):
    """
    TESTS:
    1. Получение пустого списка записей в блоге;
    2. Получение списка  записей в блоге;
    3. Создание записи в блоге.
    """
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='test@test.ru', password='123456')

        User.objects.create_user(username='test_1', password='1234567')

    def setUp(self) -> None:
        """Перед каждым тестом логиниться"""
        self.client.login(username='test_1', password='1234567')

    def test_empty_list_objects(self):
        url = '/api/v1/notes/'

        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        # Проверка на получение пустого списка
        response_data = resp.data
        expected_data = []
        self.assertEqual(expected_data, response_data)

    def test_list_objects(self):
        url = '/api/v1/notes/'

        Note.objects.create(title='Test', note='Test', author_id=1)

        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        self.assertTrue(Note.objects.get(pk=1))

    def test_login(self):
        resp = self.client.login(username='test_1', password='1234567')

        self.assertTrue(resp)

    def test_create_objects(self):
        url = '/api/v1/notes/'

        new_title = 'test_title'
        new_note = 'test_message'
        data = {
            'title': new_title,
            'note': new_note,
        }

        self.client.login(username='test_1', password='1234567')

        resp = self.client.post(url, data=data)

        expected_status_code = status.HTTP_201_CREATED
        self.assertEqual(expected_status_code, resp.status_code)

        self.assertTrue(Note.objects.get(pk=1))


class TestNoteDetailAPIView(APITestCase):
    """
    TESTS:
    1.
    """
    @classmethod
    def setUpTestData(cls):
        pass


class TestCommentNoteListCreateAPIView(APITestCase):
    """
    TESTS:
    1.
    """
    @classmethod
    def setUpTestData(cls):
        pass
