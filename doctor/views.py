from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import *


class SpecialityList(generics.ListAPIView):
    queryset = Specialization.objects.all()
    serializer_class = serializers.SpecializationSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('title',)


class DoctorList(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = serializers.DoctorSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filterset_fields = ('category', 'specializations')


class DoctorDetail(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = serializers.DoctorSerializer


class DoctorRatingCreate(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = serializers.DoctorRatingSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VideoCourseList(generics.ListAPIView):
    queryset = VideoCourse.objects.all()
    serializer_class = serializers.VideoCourseSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filterset_fields = ('category',)


class VideoCourseDetail(VideoCourseList, generics.RetrieveAPIView):
    pass


class VideoCourseCategoryList(generics.ListAPIView):
    queryset = VideoCourseCategory.objects.all()
    serializer_class = serializers.VideoCourseCategorySerializer
