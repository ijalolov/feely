from django.urls import path, include
from . import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='categories'),
    path('specialities/', views.SpecialityList.as_view(), name='specialities'),
    path('doctors/', views.DoctorList.as_view(), name='doctors'),
    path('doctor/<int:pk>/', views.DoctorDetail.as_view(), name='doctor'),
    path('doctor-rating/', views.DoctorRatingCreate.as_view(), name='doctor-rating'),
    path('video-course/', views.VideoCourseList.as_view(), name='video-course'),
    path('video-course/categories/', views.VideoCourseCategoryList.as_view(), name='video-course-categories'),
    path('video-course/<int:pk>/', views.VideoCourseDetail.as_view(), name='video-course-detail'),
]
