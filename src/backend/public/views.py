import ENV
from django.shortcuts import render

def home(request):
    return render(request, 'public/home.html', {'root': ENV.ROOT})

def question(request):
    return render(request, 'public/question.html', {'root': ENV.ROOT})
