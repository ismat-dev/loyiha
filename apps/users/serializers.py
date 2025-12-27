from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'password2', 'role']
        extra_kwargs = {'password': {'write_only': True}, 'role': {'required': True}}
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValueError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        role = validated_data.pop('role')
        user = UserProfile.objects.create_user(
            **validated_data,
            role=role
        )
        return user
    