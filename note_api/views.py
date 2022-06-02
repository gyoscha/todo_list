from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from note.models import Note, Comment
from . import serializers, filters, permissions


class CommentNoteListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]   # fixme [IsAuthenticated | permissions.OnlyAuthorEditNote], разобраться с post комментария
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset\
            .filter(
                Q(note__public=True)
            )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )


class NoteListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated | permissions.OnlyAuthorEditNote]

    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.NoteFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset\
            .filter(
                Q(author=self.request.user) |
                Q(public=True)
            ) \
            .select_related('author') \
            .prefetch_related('comments') \
            .order_by('complete_time', 'important')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        query_params = serializers.QueryParamsNoteFilterSerializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)

        status = query_params.data.get("status")
        if status:
            queryset = queryset.filter(status__in=query_params.data["status"])

        return queryset


class NoteDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated | permissions.OnlyAuthorEditNote]
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset \
            .filter(author__in=[self.request.user]) \
            .select_related('author') \
            .prefetch_related('comments')
