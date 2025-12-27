from django.contrib import admin
from .models import Answer,Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display=['student', 'test']

    
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display=['submission', 'question']