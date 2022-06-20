from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from note.models import Note, Comment
from . import serializers, filters, permissions


# class CommentNoteListCreateAPIView(ListCreateAPIView):
#     permission_classes = [IsAuthenticated | permissions.OnlyPublicNoteAddComment]
#     queryset = Comment.objects.all()
#     serializer_class = serializers.CommentSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(
#             author=self.request.user
#         )

class CommentNoteListCreateAPIView(APIView):
    def get(self, request: Request) -> Response:
        comment = Comment.objects.all()

        serializer = serializers.CommentSerializer(
            instance=comment,
            many=True,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        msg = 'Note is NOT public!!!'

        serializer = serializers.CommentSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
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
