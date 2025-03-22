# api/urls.py
from django.urls import path
from .views import news_list_create, news_detail

urlpatterns = [
    # Для списка и добавления новостей:
    path('news/', news_list_create, name='api_news_list_create'),
    # Для получения и удаления конкретной новости:
    path('news/<int:pk>/', news_detail, name='api_news_detail'),
]