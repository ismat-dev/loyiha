from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.utils import timezone

class UserProfile(AbstractUser):
    ROLE_STATUS = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('admin', 'Admin')
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_STATUS, default='admin')

    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def generate_otp(self):
        otp = str(random.randint(100000, 999999))
        self.otp_code = otp
        self.otp_created_at = timezone.now()
        self.save()
        return otp

    def otp_is_valid(self):
        if not self.otp_created_at:
            return False
        return (timezone.now() - self.otp_created_at).seconds < 300  

    def __str__(self):
        return f"{self.email} ({self.role})"

