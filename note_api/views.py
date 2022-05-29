from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from note import models
from . import serializers


class NoteListCreateAPIView(ListCreateAPIView):
    queryset = models.Note.objects.all()
    serializer_class = serializers.NoteSerializer


class NoteDetailAPIView(RetrieveUpdateDestroyAPIView):
    pass
