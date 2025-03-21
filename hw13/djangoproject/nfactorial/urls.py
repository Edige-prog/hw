
from django.contrib import admin
from django.urls import path, include
from .views import index, add, aside, check_palindrome, calc

app_name = "nfactorial"

urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
    path("<int:first>/add/<int:second>/", add),
    path("transform/<str:text>/", aside),
    path('check/<str:word>/', check_palindrome, name='check_palindrome'),

    path('calc/<int:first>/<str:operation>/<int:second>/', calc, name='calc'),
]
