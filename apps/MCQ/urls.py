from django.urls import path
from .views import *

urlpatterns = [
    path('test/create/list', TestCreateView.as_view()),
    path('tests/<int:pk>/activate/', TestActivateUpdate.as_view(), name='test-activate'),
    path('create/question/', QuestionCreateView.as_view()),
    path('test/active/', ActiveTestListView.as_view()),
]
