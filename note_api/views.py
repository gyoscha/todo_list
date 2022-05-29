from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django.db.models import Q

from note.models import Note
from . import serializers, filters


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
        if 'status' in self.request.query_params:
            queryset = filters.note_status_filter(
                queryset,
                status=self.request.query_params.get('status')
            )
        elif 'status_1' in self.request.query_params and 'status_2' in self.request.query_params:
            queryset = filters.note_multi_status_filter(
                queryset,
                status_1=self.request.query_params.get('status_1'),
                status_2=self.request.query_params.get('status_2'),
            )
        elif 'important' in self.request.query_params:
            queryset = filters.note_important_filter(
                queryset,
                important=self.request.query_params.get('important')
            )
        elif 'public' in self.request.query_params:
            queryset = filters.note_public_filter(
                queryset,
                public=self.request.query_params.get('public')
            )
        return queryset


class NoteDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset \
            .filter(author=self.request.user)
