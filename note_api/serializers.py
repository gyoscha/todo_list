from rest_framework import serializers

from note import models


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = '__all__'
        extra_kwargs = {
            'author': {'read_only': True},
        }
