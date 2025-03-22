# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='list'),
    path('<int:pk>/', views.news_detail, name='detail'),
    path('create/', views.news_create, name='create'),
    path('104/edit/', views.NewsUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.news_delete, name='news_delete'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]