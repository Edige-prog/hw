# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from news.models import News
from .serializers import NewsSerializer


@api_view(['GET', 'POST'])
def news_list_create(request):
    """
    GET: Возвращает список всех новостей.
    POST: Добавляет новую новость через API.
    """
    if request.method == 'GET':
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Сохранение новости в базу
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def news_detail(request, pk):
    """
    GET: Возвращает информацию о новости с заданным id.
    DELETE: Удаляет новость по id.
    """
    try:
        news_item = News.objects.get(pk=pk)
    except News.DoesNotExist:
        return Response({'error': 'Новость не найдена'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NewsSerializer(news_item)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        news_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)