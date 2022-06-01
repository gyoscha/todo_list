from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from note.models import Note, Comment


class TestNoteListCreateAPIView(APITestCase):
    """
    TESTS:
    1.
    """
    @classmethod
    def setUpTestData(cls):
        pass


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
