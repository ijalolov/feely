from django.urls import path, include
from . import views

urlpatterns = [
    path('tests/', views.TestList.as_view(), name='tests'),
]
