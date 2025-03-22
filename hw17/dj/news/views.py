# news/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from .models import News, Comment
from .forms import NewsForm, CommentForm
from django.views import View
from django.utils import timezone


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Добавляем пользователя в группу "default"
            default_group = Group.objects.get(name='default')
            user.groups.add(default_group)
            return redirect('login')  # переадресация на страницу логина
    else:
        form = UserCreationForm()
    return render(request, 'news/sign_up.html', {'form': form})


class NewsUpdateView(View):
    def get(self, request):
        # Получаем новость с pk=104
        news_item = get_object_or_404(News, pk=104)
        form = NewsForm(instance=news_item)
        return render(request, 'news/news_update.html', {'form': form})

    def post(self, request):
        # Получаем новость с pk=104
        news_item = get_object_or_404(News, pk=104)
        form = NewsForm(request.POST, instance=news_item)
        if form.is_valid():
            form.save()
            # Перенаправляем на детальную страницу новости с pk=104
            return redirect(news_item.get_absolute_url())
        return render(request, 'news/news_update.html', {'form': form})


@login_required
@permission_required('news.add_news', raise_exception=True)
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.created_at = timezone.now()
            # Привязываем автора новости
            news.author = request.user
            news.save()
            return redirect(news.get_absolute_url())
    else:
        form = NewsForm()
    return render(request, 'news/news_create.html', {'form': form})


# news/views.py (фрагмент news_detail)
def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    # Сортировка комментариев, например, по убыванию даты:
    comments = news_item.comments.all().order_by('-created_at')

    if request.method == 'POST':
        # Обработка формы комментария только если пользователь авторизован
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.news = news_item
                comment.created_at = timezone.now()
                comment.author = request.user
                comment.save()
                return redirect(news_item.get_absolute_url())
        else:
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        'news_item': news_item,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'news/news_detail.html', context)


@login_required
@permission_required('news.delete_news', raise_exception=True)
def news_delete(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    # Разрешаем удаление, если пользователь — автор или имеет право удаления
    if news_item.author == request.user or request.user.has_perm('news.delete_news'):
        if request.method == 'POST':
            news_item.delete()
            return redirect('news:list')
        return render(request, 'news/news_confirm_delete.html', {'news_item': news_item})
    return HttpResponseForbidden("У вас нет прав для удаления этой новости.")


@login_required
@permission_required('news.delete_comment', raise_exception=True)
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user or request.user.has_perm('news.delete_comment'):
        news_url = comment.news.get_absolute_url()
        if request.method == 'POST':
            comment.delete()
            return redirect(news_url)
        return render(request, 'news/comment_confirm_delete.html', {'comment': comment})
    return HttpResponseForbidden("У вас нет прав для удаления этого комментария.")