from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django.db.models import Q

from note.models import Note
from . import serializers


class NoteListCreateAPIView(ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset\
            .filter(
                Q(author=self.request.user) | Q(public=True)
            )\
            .order_by('complete_time', 'important')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def filter_queryset(self, queryset):
        pass


class NoteDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset \
            .filter(author=self.request.user)
