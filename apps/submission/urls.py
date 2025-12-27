from django.urls import path
from .views import *

urlpatterns = [
    path('teacher/submission', TeacherSubmissionView.as_view()),
    path('tests/<int:test_id>/start/', StarTestView.as_view()),
    path('submission/<int:submission_id>/answer/', SubmitAnswerView.as_view()),
    path('submissions/<int:pk>/submit/', SubmitView.as_view())
]
