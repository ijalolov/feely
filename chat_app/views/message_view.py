from django.contrib.auth.models import User
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from chat_app.models import Message
from chat_app.serializers import *


class MessageView(CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        print(user.sender)
        return self.create(request, *args, **kwargs)


class MyChats(generics.ListAPIView):
    serializer_class = MessageModel1Serializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        msgs = list(Message.objects.filter(
            Q(receiver=self.request.user) | Q(sender=self.request.user)
        ).values('text', 'file', 'sender', 'receiver', 'date_time').order_by('-date_time'))
        msgst = set()
        new_msg = []
        for msg in msgs:
            if msg['sender'] != self.request.user.id and msg['sender'] not in msgst:
                msgst.add(msg['sender'])
                new_msg.append(msg)
            elif msg['receiver'] != self.request.user.id and msg['receiver'] not in msgst:
                msgst.add(msg['receiver'])
                new_msg.append(msg)
        return new_msg


class CreateMessageView(CreateAPIView):
    serializer_class = MessageModelSerializer
    permission_classes = (IsAuthenticated,)


class CreateMessageView(CreateAPIView):
    parser_classes = (MultiPartParser,)
    serializer_class = MessageCreateSerializer
    permission_classes = (IsAuthenticated,)


class MessageWithView(ListAPIView):
    serializer_class = MessageModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return Message.objects.filter(
            Q(receiver=self.request.user, sender_id=user_id) |
            Q(receiver_id=user_id, sender=self.request.user)
        ).order_by('-date_time')
