from functools import partial
from django.shortcuts import get_object_or_404, render
from authentication.models import User
from .serializers import MyRefreshTokenSerializer, MyTokenObtainPairSerializer, UsersSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from datetime import date
# Create your views here.


# JWT

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyRefreshTokenSerializer

# LOGOUT


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            to_log_out = request.data['token']
            token = RefreshToken(to_log_out)
            token.blacklist()
            return Response({
                'success': True,
                'status_code': 200,
                'message': 'Logout feito com sucesso.',
            }, 200)
        except Exception as e:
            return Response({
                'success': True,
                'status_code': 400,
                'message': 'Insira o token de acesso.',
            }, 400)


# USER


class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request,  *args, **kwargs):
        serializer_user = UsersSerializer(data=request.data)
        if serializer_user.is_valid(raise_exception=True):
            birth_date = serializer_user.validated_data.get("birth_date")
            age = (date.today() - birth_date).days / 365
            if age < 18:
                msg = {
                    'success': False,
                    'status_code': 400,
                    'message': 'Erro na verificação da idade do usúario.',
                    'data': None,
                }
                return Response(msg, status=400)
            password = serializer_user.validated_data.pop('password', None)
            instance = serializer_user.save()
            if password is not None:
                instance.set_password(password)
                username = serializer_user.validated_data.get('username')
                obj = get_object_or_404(User, username=username)
                instance.owner = obj
            serializer_user.save()
            data = serializer_user.data
            user_data = data
            data = {
                'success': True,
                'status_code': 201,
                'message': 'Usúario criado com sucesso.',
                'data': {
                    'id': user_data['id']
                },
            }
            return Response(data, status=201)
