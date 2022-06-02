from datetime import timedelta, datetime

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from note.models import Note, Comment


class TestNoteListCreateAPIView(APITestCase):
    """
    TESTS:
    1. Получение пустого списка записей в блоге;
    2. Получение списка записей в блоге;
    3. Создание записи в блоге.
    """
    @classmethod
    def setUpTestData(cls):
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
    1. Получение существующей записи в блоге;
    2. Получение несуществующей записи в блоге;
    3. Обновление существующей записи в блоге;
    4. Обновление несуществующей записи в блоге.
    5. Частичное обновление записи
    6. Удаление записи
    7. Получение существующей записи, но под другим пользователем
    """

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test_1', password='1234567')
        Note.objects.create(title='TEST_title', note='TEST_msg', author_id=1)
        Note.objects.create(title='TEST_title_2', note='TEST_msg_2', author_id=1)

        User.objects.create_user(username='test_2', password='1234567')
        Note.objects.create(title='TEST_title_3', note='TEST_msg_3', author_id=2)

    def setUp(self) -> None:
        """Перед каждым тестом логиниться"""
        self.client.login(username='test_1', password='1234567')

    @classmethod
    def get_date_create_at(cls):
        now = datetime.now()
        create_at = now.strftime('%d %B %Y - %H:%M:%S')

        return create_at

    @classmethod
    def get_date_complete_time(cls):
        complete = datetime.now() + timedelta(days=1)
        create_at = complete.strftime('%d %B %Y - %H:%M:%S')

        return create_at

    def test_retrieve_existing_object(self):
        pk = 1
        url = f'/api/v1/notes/{pk}'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "id": 1,
            "title": "TEST_title",
            "note": "TEST_msg",
            "status": {
                "value": "AC",
                "display": "Активно"
            },
            "important": False,
            "public": False,
            "complete_time": f'{self.get_date_complete_time()}',
            "create_at": f'{self.get_date_create_at()}',
            "author": "test_1",
            "comments": []
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_retrieve_non_existent_object(self):
        pk = 11
        url = f'/api/v1/notes/{pk}'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_404_NOT_FOUND
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "detail": "Not found."
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_update_existing_object(self):
        pk = 1
        url = f'/api/v1/notes/{pk}'

        put_data = {
            'title': 'TEST_title_PUT',
            'note': 'TEST_msg_PUT',
        }

        resp = self.client.put(url, put_data)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "id": 1,
            "title": "TEST_title_PUT",
            "note": "TEST_msg_PUT",
            "status": {
                "value": "AC",
                "display": "Активно"
            },
            "important": False,
            "public": False,
            "complete_time": f'{self.get_date_complete_time()}',
            "create_at": f'{self.get_date_create_at()}',
            "author": "test_1",
            "comments": []
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_update_non_existent_object(self):
        pk = 11
        url = f'/api/v1/notes/{pk}'

        put_data = {
            'title': 'TEST_title_PUT',
            'note': 'TEST_msg_PUT',
        }
        resp = self.client.put(url, put_data)

        expected_status_code = status.HTTP_404_NOT_FOUND
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "detail": "Not found."
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_patch_title(self):
        pk = 2
        url = f'/api/v1/notes/{pk}'

        patch_data_1 = {
            'title': 'TEST_title_patch',
        }

        resp = self.client.patch(url, patch_data_1)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "id": 2,
            "title": "TEST_title_patch",
            "note": "TEST_msg_2",
            "status": {
                "value": "AC",
                "display": "Активно"
            },
            "important": False,
            "public": False,
            "complete_time": f'{self.get_date_complete_time()}',
            "create_at": f'{self.get_date_create_at()}',
            "author": "test_1",
            "comments": []
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_patch_note(self):
        pk = 1
        url = f'/api/v1/notes/{pk}'

        patch_data_2 = {
            'note': 'TEST_msg_patch',
        }

        resp = self.client.patch(url, patch_data_2)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "id": 1,
            "title": "TEST_title",
            "note": "TEST_msg_patch",
            "status": {
                "value": "AC",
                "display": "Активно"
            },
            "important": False,
            "public": False,
            "complete_time": f'{self.get_date_complete_time()}',
            "create_at": f'{self.get_date_create_at()}',
            "author": "test_1",
            "comments": []
        }
        self.assertDictEqual(expected_data, resp.data)

    def test_delete(self):
        pk = 1
        url = f'/api/v1/notes/{pk}'

        resp = self.client.delete(url)

        expected_status_code = status.HTTP_204_NO_CONTENT
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = None

        self.assertEqual(expected_data, resp.data)

    def test_retrieve_object_not_auth(self):
        pk = 3
        url = f'/api/v1/notes/{pk}'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_404_NOT_FOUND
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "detail": "Not found."
        }

        self.assertDictEqual(expected_data, resp.data)


class TestCommentNoteListCreateAPIView(APITestCase):
    """
    TESTS:
    1. Получение пустого списка публичных записей
    2. Получение списка только публичных записей
    3. Создание комментария к записи
    """
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test_1', password='1234567')

        Note.objects.create(title='TEST_title', note='TEST_msg', author_id=1, public=True)
        Note.objects.create(title='TEST_title_2', note='TEST_msg_2', author_id=1)

    def setUp(self) -> None:
        """Перед каждым тестом логиниться"""
        self.client.login(username='test_1', password='1234567')

    def test_empty_list(self):
        url = '/api/v1/notes/comments/'

        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        # Проверка на получение пустого списка
        response_data = resp.data
        expected_data = []
        self.assertEqual(expected_data, response_data)

    def test_list_objects(self):
        url = '/api/v1/notes/comments/'

        Comment.objects.create(note_id=1, rating=2, author_id=1)

        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        self.assertTrue(Comment.objects.get(pk=1))

    def test_list_objects_public(self):
        url = '/api/v1/notes/comments/'

        Comment.objects.create(note_id=1, rating=5, author_id=1)
        Comment.objects.create(note_id=2, rating=2, author_id=1)

        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = [{
            "id": 1,
            "rating": 5,
            "author": 1,
            "note": 1
        }]

        self.assertListEqual(expected_data, resp.data)

    def test_post_comment(self):
        url = '/api/v1/notes/comments/'

        rating = 5
        note = 1
        data = {
            "rating": rating,
            "note": note,
        }

        resp = self.client.post(url, data=data)

        expected_status_code = status.HTTP_201_CREATED
        self.assertEqual(expected_status_code, resp.status_code)

        self.assertTrue(Comment.objects.get(pk=1))
