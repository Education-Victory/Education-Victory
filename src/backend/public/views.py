import ENV
from django.shortcuts import render

def home(request):
    # HTML for home page
    return render(request, 'public/home.html', {'root': ENV.ROOT})

def question(request):
    # HTML for question list page
    return render(request, 'public/question.html', {'root': ENV.ROOT})

def question_detail(request, question_name, category_name):
    # HTML for question detail page
    return render(request, 'public/question_detail.html',
        {'root': ENV.ROOT, 'question_name': question_name, 'category_name': category_name, 'user_id': request.user.id})

