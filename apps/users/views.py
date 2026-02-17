from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OTP
from .serializers import SendOTPSerializer, VerifyOTPSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import random

User = get_user_model()


class SendOTPView(APIView):

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        code = str(random.randint(100000, 999999))

        OTP.objects.create(phone=phone, code=code)

        # ⚠ فقط للتطوير — نرجع الكود في response
        return Response({
            "message": "OTP sent",
            "otp": code
        })


class VerifyOTPView(APIView):

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        otp = OTP.objects.filter(phone=phone, code=code).last()

        if not otp or not otp.is_valid():
            return Response({"error": "Invalid OTP"}, status=400)

        user, created = User.objects.get_or_create(phone=phone)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        })
