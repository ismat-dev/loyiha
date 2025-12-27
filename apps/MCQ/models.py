from django.db import models
from datetime import timedelta
from apps.users.models import UserProfile

class Test(models.Model):
    title = models.CharField(max_length=150)
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    duration_minutes = models.DurationField(default=timedelta(minutes=20))
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    OPTIONS = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField()
    option = models.CharField(choices=OPTIONS, default='A')
    correct_option = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test.title} - {self.text[:20]}"