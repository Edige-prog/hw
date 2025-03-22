# project/urls.py
from django.contrib import admin
from django.urls import path, include
from news import views as news_views  # регистрация разместим в приложении news

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # маршруты login, logout, password_change и т.д.
    path('sign-up/', news_views.sign_up, name='sign_up'),
]