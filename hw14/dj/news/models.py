# news/models.py
from django.db import models
from django.urls import reverse

class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название новости')
    content = models.TextField(verbose_name='Текст новости')
    created_at = models.DateTimeField(verbose_name='Дата создания')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # После создания будет перенаправление на страницу детального просмотра новости.
        return reverse('news:detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments', verbose_name='Новость')
    content = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(verbose_name='Дата создания')

    def __str__(self):
        return f'Комментарий к {self.news.title}'