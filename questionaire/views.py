from django.shortcuts import render,redirect
from django import http
from .models import Questionaire, QuestionaireQuestion, QuestionaireOption, QuestionaireSubmission
# Create your views here.
def index(request, theme):
    # return http.HttpResponse("THIS IS A QUESTIONAIRE PAGE")
    
    curr_theme_ins = Questionaire.objects.get(theme=theme)
    all_questions_ins = curr_theme_ins.questionairequestion_set.all()
    all_choices_ins = {}
    for question in all_questions_ins:
        all_choices_ins[question] = question.questionaireoption_set.all()
    context = {"theme": curr_theme_ins, "choices": all_choices_ins} 
    
    if request.method == 'POST':
        
        for qid in request.POST:
            if qid.isdigit():
                q = QuestionaireQuestion.objects.get(pk=qid)
                o = QuestionaireOption.objects.get(question = q, option = request.POST[qid])
                qs = QuestionaireSubmission(question = q, selected_choice = o)
                qs.save()
            
        return redirect('success')

    return render(request, "Questionaire/index.html", context)

def success(request):
    return render(request, "Questionaire/success.html")

def questionaire_selection(request):
    context = {"questionaires" : Questionaire.objects.all()}
    return render(request, "Questionaire/home.html", context)
