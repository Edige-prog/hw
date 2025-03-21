from django.contrib import admin

# Register your models here.
# news/admin.py
from django.contrib import admin
from .models import News, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 5

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'has_comments')
    inlines = [CommentInline]

admin.site.register(News, NewsAdmin)