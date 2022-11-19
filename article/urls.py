from django.urls import path, include
from . import views

urlpatterns = [
    path('article/', views.ArticleView.as_view(), name='article'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('adv/', views.AdvView.as_view(), name='adv'),
]
