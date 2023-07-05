import ENV
from django.shortcuts import render
from django.http import JsonResponse

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

def evaluation(request, type):
    if type == 'simple':
        return render(request, 'public/evaluation/simple.html')
    else:
        return render(request, 'public/evaluation/detail.html')

def evaluation_simple(request):
    # Use three simple questions for simple evaluation to determine which level the user belongs to
    question_lst = {
        'data': [
        {
            'title': 'How many years of programming experience do you have?',
            'description': '',
            'type': 'single',
            'choice': [
                {
                    'text': '< 1 years',
                    'value': 0
                },
                {
                    'text': '1 - 3 years',
                    'value': 20
                },
                {
                    'text': '3 - 6 years',
                    'value': 30
                },
                {
                    'text': '> 6 years',
                    'value': 40
                },
            ]
        },
        {
            'title': 'How many algorithm problems have you solved?',
            'description': '',
            'type': 'single',
            'choice': [
                {
                    'text': '< 50',
                    'value': 0
                },
                {
                    'text': '50 - 100',
                    'value': 20
                },
                {
                    'text': '100 - 300',
                    'value': 30
                },
                {
                    'text': '> 300',
                    'value': 40
                },
            ]
        },
        {
            'title': 'When do you expect to begin the interview?',
            'description': '',
            'type': 'single',
            'choice': [
                {
                    'text': '< 2 weeks',
                    'value': 0
                },
                {
                    'text': '2 weeks - 1 month',
                    'value': 20
                },
                {
                    'text': '1 month - 3 months',
                    'value': 30
                },
                {
                    'text': '> 3 months',
                    'value': 40
                },
            ]
        }]
    }
    return JsonResponse(question_lst)
