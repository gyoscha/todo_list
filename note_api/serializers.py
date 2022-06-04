from datetime import datetime

from rest_framework import serializers

from note import models


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'
        read_only_fields = ("author",)


class NoteSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    comments = CommentSerializer(many=True, read_only=True)

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


class QueryParamsNoteFilterSerializer(serializers.Serializer):
    status = serializers.ListField(
        child=serializers.ChoiceField(choices=models.Note.Status.choices), required=False,
    )
