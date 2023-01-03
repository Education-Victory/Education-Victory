from django.contrib import admin

# Register your models here.
from .models import Questionaire
from .models import QuestionaireQuestion
from .models import QuestionaireOption
from .models import QuestionaireSubmission

admin.site.register(Questionaire)
admin.site.register(QuestionaireQuestion)
admin.site.register(QuestionaireOption)
admin.site.register(QuestionaireSubmission)