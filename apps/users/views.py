from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
# local
from .models import UserProfile
from .serializers import UserProfileSerializers

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializers
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            email = serializers.validated_data['email']
            if UserProfile.objects.filter(email=email).exists():
                return Response({'error': 'User with this email already exists'}, status=400)
            user = UserProfile.objects.create_user(
                username=serializers.validated_data['username'],
                email=email,
                password=serializers.validated_data['password'],
                role=serializers.validated_data['role'],
                is_active=False
            )
            user.generate_otp()

            send_mail(
                'Your Registration OTP Code',
                f'Your OTP code is: {user.otp_code}',
                'ismatismoilov709@gmail.com', 
                [email],
                fail_silently=False,
            )
            return Response(
                {'message': 'OTP sent to your email. Please verify.'},
                status=200)
        return Response(serializers.errors, status=400)

class UserVerifyLogin(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')

        try:
            user = UserProfile.objects.get(email=email, otp_code=otp_code)
            if not user.otp_is_valid():
                return Response({'error': 'OTP expired'}, status=400)
            user.is_active = True
            user.otp_code = None
            user.otp_created_at = None
            user.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Account verified & logged in',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Invalid email or OTP'},
                status=400
            )

# log out
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logges out'}, status=204)
        except Exception as e:
            return Response({'detail': 'Invalid token or missing token'}, status=400)