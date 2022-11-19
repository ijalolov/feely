import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat_app.authentication import BearerAuthentication
from chat_app.serializers import UsersWithMessageSerializer
from users.serializers import ProfileSerializer as UserSerializer


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        """

        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        self.__change_status(user)
        serialize_user = UserSerializer(user, many=False)
        return Response({
            'token': token.key,
            'user': serialize_user.data,
        })

    def __change_status(self, user: User):
        """
        @param user:
        """
        profile = user.profile
        profile.online = True
        profile.save()
        notify_others(user)


class LogOutView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, BearerAuthentication]

    def post(self, request, format=None):
        profile = request.user.profile
        profile.online = False
        profile.save()
        notify_others(request.user)
        return Response({'message': 'logout'})


def notify_others(user: User):
    """

    @param user:
    @return:
    """
    serializer = UserSerializer(user, many=False)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notification', {
            'type': 'user_online',
            'message': serializer.data
        }
    )


def test_socket(request):
    # users = User.objects.all()
    # return render(request, template_name='test.html', context={'users': users})
    # serializer = UserSerializer(user, many=False)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'chat_rifat', {
            'type': 'new_call',
            'message': {
                'receiver': 'ritu',
                'sender': 'rifat'
            }
        }
    )
    return HttpResponse("hello world")
