# news/tests.py
from django.test import TestCase
from django.utils import timezone
from .models import News, Comment
from django.urls import reverse

class NewsModelTest(TestCase):
    def test_has_comments_true(self):
        news = News.objects.create(
            title="Тестовая новость",
            content="Контент новости",
            created_at=timezone.now()
        )
        Comment.objects.create(
            news=news,
            content="Первый комментарий",
            created_at=timezone.now()
        )
        self.assertTrue(news.has_comments())

    def test_has_comments_false(self):
        news = News.objects.create(
            title="Тестовая новость без комментариев",
            content="Контент новости",
            created_at=timezone.now()
        )
        self.assertFalse(news.has_comments())


class NewsViewsTest(TestCase):
    def setUp(self):
        # Создаем две новости с разными датами создания
        self.news1 = News.objects.create(
            title="Старое сообщение",
            content="Содержимое старого сообщения",
            created_at=timezone.now() - timezone.timedelta(days=1)
        )
        self.news2 = News.objects.create(
            title="Новое сообщение",
            content="Содержимое нового сообщения",
            created_at=timezone.now()
        )
        # Создаем новость с pk=102 для тестов детального просмотра
        self.news_detail = News.objects.create(
            id=102,
            title="Детальная новость",
            content="Полное содержание детальной новости",
            created_at=timezone.now()
        )
        # Создаем несколько комментариев для новости с pk=102
        Comment.objects.create(
            news=self.news_detail,
            content="Первый комментарий",
            created_at=timezone.now() - timezone.timedelta(minutes=10)
        )
        Comment.objects.create(
            news=self.news_detail,
            content="Второй комментарий",
            created_at=timezone.now() - timezone.timedelta(minutes=5)
        )

    def test_news_list_order(self):
        url = reverse('news:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Проверяем, что новости отсортированы в порядке убывания даты (новое сообщение первым)
        news_list = response.context['news_list']
        self.assertEqual(news_list.first(), self.news2)

    def test_news_detail_view(self):
        url = reverse('news:detail', kwargs={'pk': self.news_detail.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.news_detail.title)
        self.assertContains(response, self.news_detail.content)

    def test_news_detail_comments_order(self):
        url = reverse('news:detail', kwargs={'pk': self.news_detail.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        comments = response.context['comments']
        # Ожидаем, что комментарии отсортированы по убыванию даты (первым должен быть более новый)
        self.assertGreater(comments.first().created_at, comments.last().created_at)