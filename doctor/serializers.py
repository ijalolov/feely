from django.conf import settings
from django.db.models import Avg
from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Category
        exclude = ('order',)

    def get_logo(self, obj):
        try:
            return settings.HOST + obj.logo.url
        except:
            return None


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    specializations = SpecializationSerializer(many=True)
    avg_rating = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = '__all__'

    def get_avg_rating(self, obj):
        return DoctorRating.objects.filter(doctor=obj).aggregate(rating=Avg('rating'))['rating'] or 0

    def get_total_rating(self, obj):
        return DoctorRating.objects.filter(doctor=obj).count()

    def get_user_rating(self, obj):
        try:
            return DoctorRating.objects.filter(doctor=obj, user=self.context['request'].user).first().rating
        except:
            return None


class DoctorRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRating
        exclude = ('user',)

    def validate(self, attrs):
        if DoctorRating.objects.filter(user=self.context['request'].user, doctor=attrs['doctor']).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв')
        return attrs


class VideoCourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCourseCategory
        fields = '__all__'


class VideoCourseSerializer(serializers.ModelSerializer):
    category = VideoCourseCategorySerializer()

    class Meta:
        model = VideoCourse
        fields = '__all__'



