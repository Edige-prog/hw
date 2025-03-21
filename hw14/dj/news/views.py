# news/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Comment
from .forms import NewsForm, CommentForm
from django.utils import timezone

def news_list(request):
    # Получаем список новостей в порядке убывания (новые первыми)
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'news_list': news_list})


def news_detail(request, pk):
    # Получаем новость по переданному pk или 404, если не существует
    news_item = get_object_or_404(News, pk=pk)
    # Получаем все комментарии, связанные с новостью, сортируя по дате создания
    comments = news_item.comments.all().order_by('created_at')

    if request.method == 'POST':
        # Обработка отправки формы для нового комментария
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news = news_item
            comment.created_at = timezone.now()
            comment.save()
            # Перенаправляем на ту же страницу (чтобы форма была пустой и обновился список комментариев)
            return redirect(news_item.get_absolute_url())
    else:
        comment_form = CommentForm()

    context = {
        'news_item': news_item,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'news/news_detail.html', context)


def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            # Устанавливаем дату создания как текущее время
            news.created_at = timezone.now()
            news.save()
            # Перенаправляем на детальную страницу созданной новости
            return redirect(news.get_absolute_url())
    else:
        form = NewsForm()

    return render(request, 'news/news_create.html', {'form': form})