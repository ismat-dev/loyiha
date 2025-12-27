from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import serializers
# local
from apps.users.models import UserProfile
from apps.users.permissions import IsStudent, IsTeacher
from .models import Test,  Question
from .serializers import Questionerializers, TestSerializer, TestActivateSerializer, ActiveTestSerializer
from rest_framework.exceptions import ValidationError

class TestCreateView(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

# create question
class QuestionCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = Questionerializers
    permission_classes  = [IsAuthenticated, IsTeacher]

# to do active created test
class TestActivateUpdate(generics.UpdateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestActivateSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return Test.objects.all()

class TestRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, IsTeacher]




class ActiveTestListView(generics.ListAPIView):
    serializer_class = ActiveTestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Test.objects.filter(is_active=True)