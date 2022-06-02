from rest_framework.permissions import BasePermission, SAFE_METHODS

from note import models


class OnlyAuthorEditNote(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.author


class OnlyPublicNoteAddComment(BasePermission):
    def has_object_permission(self, request, view, obj: models.Comment):
        if request.method in SAFE_METHODS:
            return True

        return obj.note.public
