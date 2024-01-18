import random
import string

import jwt
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from .email import send_email
from .models import User
from .serializers import UserCreateSerializer, UserLoginSerializer, UserEditSerializer, GenerateNewSerializer


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


# Create your views here.
class RegisterView(APIView):
    # permission_classes = [IsSuperUser]

    @swagger_auto_schema(request_body=UserCreateSerializer)
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request):
        email, password = request.data.get('email'), request.data.get('password')
        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            raise AuthenticationFailed('Incorrect email or password!')

        login(request, user)
        user.refresh_from_db()
        user.verification_code = random.randint(100000, 999999)
        user.save()

        send_email.delay(user.email, user.verification_code)
        messages.success(request, 'Verification code sent to your email. Please check your mail.')

        serializer = UserLoginSerializer(user)

        expiration_time = timezone.now() + timezone.timedelta(minutes=60)
        payload = {'id': user.id, 'exp': expiration_time, 'iat': timezone.now()}
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response_data = {'user': serializer.data, 'jwt': token}
        response = Response(response_data, status=status.HTTP_200_OK)
        response.set_cookie(key='jwt', value=token, httponly=True)

        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # Specify the list of acceptable algorithms (HS256 in this case)
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserCreateSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class VerifyForLoginApi(APIView):

    def post(self, request, code):

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # Specify the list of acceptable algorithms (HS256 in this case)
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        # Compare the verification code from the request with the one stored in the user model
        if user.verification_code == code:
            # Verification code matches, set is_staff to True
            user.is_staff = True
            user.save(update_fields=['is_staff'])

            return Response({'detail': 'Verification successful. User is now staff.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Verification code does not match.'}, status=status.HTTP_400_BAD_REQUEST)


class EditCurrrentUserData(APIView):

    @swagger_auto_schema(request_body=UserEditSerializer)
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # Specify the list of acceptable algorithms (HS256 in this case)
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        if user and user.is_staff is True:
            serializer = UserLoginSerializer(data=request.data, instance=user, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            verification_code = ''.join([str(random.randint(100000, 999999))])
            user.verification_code = verification_code
            user.save()

            send_email.delay(user.email, verification_code)
            messages.success(request, 'Verification code sent to your email. Please check your mail.')

            return Response({'detail': 'User data updated successfully.'})


class VerifyForActivateApi(APIView):

    def post(self, request, code):

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        if user.verification_code == code:
            user.is_active = True
            user.save(update_fields=['is_active'])

            return Response({'detail': 'Verification successful. User is now active.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Verification code does not match.'}, status=status.HTTP_400_BAD_REQUEST)


class GenerateNewPassword(APIView):

    @swagger_auto_schema(request_body=GenerateNewSerializer)
    def post(self, request):
        serializer = GenerateNewSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse({'message': 'Invalid data provided'}, status=400)

        try:
            email = serializer.validated_data.get('email')
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

        new_password = ''.join(random.choices(string.digits, k=6))
        user.password = make_password(new_password)
        user.save()

        response_data = {
            'generated_password': new_password,
        }
        return JsonResponse(response_data)
