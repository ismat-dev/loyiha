from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Answer, Submission
from .serializers import AnswerSerializer, SubmissionSerializer, SubmissionSubmitSerializer
from apps.users.permissions import IsTeacher, IsStudent
from datetime import timezone
class TeacherSubmissionView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return Submission.objects.filter(test__teacher=self.request.user)

class StarTestView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        student = self.request.user
        test = serializer.validated_data['test']

        if Submission.objects.filter(student=student, test=test).exists():
            raise ValidationError("Siz bu tests ni boshlagansiz")
        serializer.save(student=student, status="in_progress")

class SubmitAnswerView(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        submission = serializer.validated_data['submission']

        if submission.student != self.request.user:
            raise ValidationError("Siz bu submission uchun javob bera olmaysiz.")
        if submission.status != 'in_progress':
            raise ValidationError("Submission allaqachon topshirilgan.")
        if timezone.now() > submission.started_at + submission.test.duration_minutes:
            raise ValidationError("Test vaqti tugagan.")
        
        serializer.save()

class SubmitView(generics.UpdateAPIView):
    serializer_class = SubmissionSubmitSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user) 