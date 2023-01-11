from django.shortcuts import render

def home(request):
    return render(request, 'public/home.html')
