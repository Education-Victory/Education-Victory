import ENV
from django.shortcuts import render

def home(request):
    return render(request, 'public/home.html', {'root': ENV.ROOT})

def question(request):
    return render(request, 'public/question.html', {'root': ENV.ROOT})


def question_detail(request, question_name, category_name):
    return render(request, 'public/question_detail.html',
        {'root': ENV.ROOT, 'question_name': question_name, 'category_name': category_name})

