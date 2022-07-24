from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

def get_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegisterSLR
    def post(self, request, format=None):
        slr = self.serializer_class(data=request.data)
        slr.is_valid(raise_exception=True)
        slr.save()
        return Response({'Msg':'Registraion Successful ...', 'Data':slr.data}, status=status.HTTP_201_CREATED)

class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSLR
    def post(self, request, format=None):
        slr = self.serializer_class(data=request.data)
        slr.is_valid(raise_exception=True)
        user = authenticate(email=slr.data['email'].lower(), password=slr.data.get('password'))
        if user is not None:
            return Response({'Msg':'Login Successful ...', 'Email':str(user), 'Tokens':get_tokens(user)}, status=status.HTTP_200_OK)
        return Response({'Non_field_errors':'Email or Password is not Valid!'}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        slr = UserProfileSLR(request.user)
        return Response({'Msg':f'{slr.data["name"]} Data', 'Profile':slr.data}, status=status.HTTP_200_OK)

class UserChangePasswordView(GenericAPIView):
    serializer_class = UserChangePasswordSLR
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        slr = self.serializer_class(data=request.data, context={'user':request.user})
        slr.is_valid(raise_exception=True)
        return Response({'Msg':'Password Change Successfully'}, status=status.HTTP_200_OK)

class SendEmailResetPasswordView(GenericAPIView):
    serializer_class = SendEmailResetPasswordSLR
    def post(self, request, format=None):
        slr = self.serializer_class(data=request.data)
        slr.is_valid(raise_exception=True)
        return Response({'Msg':'Password Reset Link sent. Please Check Your Email'}, status=status.HTTP_200_OK)

class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSLR
    def post(self, request, uid, token, format=None):
        slr = self.serializer_class(data=request.data, context={'uid':uid, 'token':token})
        slr.is_valid(raise_exception=True)
        return Response({'Msg':'Password Change Successfully...'}, status=status.HTTP_200_OK)