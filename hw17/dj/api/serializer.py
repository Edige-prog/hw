# api/serializers.py
from rest_framework import serializers
from news.models import News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        # Поля, которые будут возвращаться через API. Если поле author – ForeignKey, можно вернуть, например, его id.
        fields = ['id', 'title', 'content', 'created_at', 'author']