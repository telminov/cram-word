from rest_framework import serializers
from core import models


class YaDictFromRus(serializers.Serializer):
    rus_word = serializers.CharField()
    lang = serializers.PrimaryKeyRelatedField(queryset=models.Language.objects.all())


class YaDictToRus(serializers.Serializer):
    word = serializers.CharField()
    lang = serializers.PrimaryKeyRelatedField(queryset=models.Language.objects.all())
