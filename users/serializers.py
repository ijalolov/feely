from django.conf import settings
from rest_framework import serializers

from doctor.serializers import DoctorSerializer
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'full_name')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            validated_data['username'], password=validated_data['password'],
            full_name=validated_data['full_name'], is_active=True,
            email=validated_data['username']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    pic = serializers.SerializerMethodField()
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'full_name', 'pic', 'email', 'doctor', 'about'
        )

    def get_pic(self, obj):
        try:
            return settings.HOST + obj.pic.url
        except Exception as e:
            print(e)
            return None


class ProfileShortSerializer(serializers.ModelSerializer):
    pic = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'full_name', 'pic', 'email', 'about'
        )

    def get_pic(self, obj):
        try:
            return settings.HOST + obj.pic.url
        except Exception as e:
            print(e)
            return None