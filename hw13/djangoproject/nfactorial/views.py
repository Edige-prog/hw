from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello, nfactorial school!")


def add(request, first, second):
    return HttpResponse(f"{first} plus {second} = {first + second}")

def aside(request, text):
    return HttpResponse(text.upper())


def check_palindrome(request, word):
    # Приводим слово к нижнему регистру, если требуется игнорировать регистр
    normalized_word = word.lower()
    is_palindrome = normalized_word == normalized_word[::-1]
    return JsonResponse({'result': is_palindrome})


def calc(request, first, operation, second):
    if operation == 'add':
        result = first + second
    elif operation == 'sub':
        result = first - second
    elif operation == 'mult':
        result = first * second
    elif operation == 'div':
        if second == 0:
            return JsonResponse({'error': 'Division by zero'}, status=400)
        result = first / second
    else:
        return JsonResponse({'error': f'Unsupported operation: {operation}'}, status=400)

    return JsonResponse({'result': result})