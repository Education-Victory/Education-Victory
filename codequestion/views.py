from django.shortcuts import render, redirect
from .models import CodeQuestionItem
from .forms import CodeQuestionItemForm
# Create your views here.
def index(request):
    codequestions = CodeQuestionItem.objects.all()
    context = {"questions": codequestions}
    return render(request, "Codequestion/list.html", context)


def update(request, pk):
    question = CodeQuestionItem.objects.get(id=pk)
    form = CodeQuestionItemForm(instance = question)
    context = {'form': form, 'question': question}
    if request.method == 'POST':
        form = CodeQuestionItemForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('/codequestion')
    return render(request, "Codequestion/update.html", context)

def search(request):
    query = request.GET.get('query')
    if query:
        items = CodeQuestionItem.objects.filter(title__contains=query)
    else:
        items = CodeQuestionItem.objects.all()
    return render(request, "Codequestion/list.html", {'questions': items})