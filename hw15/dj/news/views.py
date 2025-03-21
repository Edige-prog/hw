# news/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import News
from .forms import NewsForm

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