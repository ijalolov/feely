import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers

from chat_app.models import Message
from users.models import User
from users.serializers import ProfileSerializer, ProfileShortSerializer


class MessageSerializer(serializers.Serializer):
    text = serializers.CharField()
    read = serializers.BooleanField(read_only=True)
    date_time = serializers.DateTimeField(required=False)
    sender_id = serializers.IntegerField(read_only=True)
    receiver = serializers.SlugField(write_only=True)

    def create(self, validated_data):
        try:
            user = User.objects.get(username=validated_data['receiver'])
            message = Message()
            message.text = validated_data['text']
            message.sender = self.context['request'].user
            message.receiver = user
            message.save()
            self.__broadcast(message)
            return validated_data
        except Exception as e:
            raise Exception('Error', e)

    def __broadcast(self, message: Message):
        serializer = MessageModelSerializer(message, many=False)
        n_message = serializer.data
        n_message['read'] = False
        print(n_message)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_%s' % message.receiver.username, {
                'type': 'new_message',
                'message': n_message
            }
        )


class MessageModelSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)
    is_my = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('text', 'file', 'sender', 'date_time', 'is_my')

    def get_is_my(self, obj):
        return obj.sender == self.context['request'].user

    def get_file(self, obj):
        try:
            return settings.MEDIA_URL + obj.file.url
        except:
            return None


class MessageModel1Serializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    is_my = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('text', 'file', 'sender', 'receiver', 'date_time', 'is_my', 'last_message')

    def get_is_my(self, obj):
        return obj['sender'] == self.context['request'].user.id

    def get_file(self, obj):
        try:
            return settings.MEDIA_URL + obj.file.url
        except:
            return None

    def get_sender(self, obj):
        print(obj)
        sender = User.objects.get(id=obj['sender'])
        return ProfileShortSerializer(sender, many=False).data

    def get_receiver(self, obj):
        receiver = User.objects.get(id=obj['receiver'])
        return ProfileShortSerializer(receiver, many=False).data

    def get_last_message(self, obj):
        lst = Message.objects.filter(Q(sender=self.context['request'].user) | Q(receiver=self.context['request'].user)).order_by('-date_time').first()
        return {
            'text': lst.text,
            'file': settings.HOST + lst.file.url if lst.file else None,
        }


class UsersWithMessageSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('full_name', 'username', 'pic', 'online', 'messages')

    def get_messages(self, obj):
        messages = Message.objects.filter(
            Q(receiver=obj, sender=self.context['request'].user) |
            Q(sender=obj, receiver=self.context['request'].user)).prefetch_related('sender', 'receiver')
        serializer = MessageModelSerializer(messages.order_by('date_time'), many=True)
        return serializer.data


class MessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('text', 'file', 'receiver')

    def validate(self, attrs):
        if attrs['receiver'] == self.context['request'].user:
            raise serializers.ValidationError('You cannot send message to yourself')
        return attrs

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return Message.objects.create(**validated_data)

    def get_file(self, obj):
        try:
            return settings.HOST + obj.file.url
        except Exception as e:
            return None
