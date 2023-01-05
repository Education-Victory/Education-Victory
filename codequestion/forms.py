from django import forms
from django.forms import widgets 
from .models import CodeQuestionItem

class CodeQuestionItemForm(forms.ModelForm):
    class Meta:
        model = CodeQuestionItem
        fields = ['completed']
        widgets = {'completed': forms.CheckboxInput}
        
    