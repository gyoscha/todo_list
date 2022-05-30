from datetime import datetime

from rest_framework import serializers

from note import models


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = '__all__'
        extra_kwargs = {
            'author': {'read_only': True},
        }

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
