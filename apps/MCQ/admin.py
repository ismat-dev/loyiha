from django.contrib import admin
from .models import Test, Question

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display=['title', 'teacher', 'duration_minutes']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display=['test', 'text', 'option']