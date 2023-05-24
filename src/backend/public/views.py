import os
from django.shortcuts import render

# get ROOT from environment variable
ROOT = os.environ.get('ROOT')


def home(request):
    return render(request, 'public/home.html', {'root': ROOT})


def question(request):
    return render(request, 'public/question.html', {'root': ROOT})


def question_detail(request, question_name, category_name):
    return render(request, 'public/question_detail.html',
                  {'root': ROOT, 'question_name': question_name, 'category_name': category_name})
