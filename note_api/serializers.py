from datetime import datetime

from rest_framework import serializers

from note import models


class CommentPostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = models.Comment
        fields = (
            'id', 'note', 'rating',
            'author'
        )


class NoteSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    comments = CommentPostSerializer(many=True, read_only=True)

    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj: models.Note):
        return {
            'value': obj.status,
            'display': obj.get_status_display()
        }

    class Meta:
        model = models.Note
        fields = (
            'id', 'title', 'note', 'status', 'important', 'public', 'complete_time', 'create_at',
            'author', 'comments'
        )

    def to_representation(self, instance):
        """ Переопределение вывода. Меняем формат даты в ответе """
        ret = super().to_representation(instance)
        # Конвертируем строку в дату по формату
        create_at = datetime.strptime(ret['create_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        complete_time = datetime.strptime(ret['complete_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # Конвертируем дату в строку в новом формате
        ret['create_at'] = create_at.strftime('%d %B %Y - %H:%M:%S')
        ret['complete_time'] = complete_time.strftime('%d %B %Y - %H:%M:%S')
        return ret
