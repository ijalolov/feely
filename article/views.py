from django.conf import settings
from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from article.models import Article, Adv
from users.serializers import ProfileSerializer


class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


class ArticleView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('title',)


class ArticleDetailView(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class AdvView(generics.GenericAPIView):

    def get(self, request):
        adv = Adv.get_solo()
        return Response({
            'link': adv.link,
            'images': [settings.HOST + image.image.url for image in adv.images.all()]
        })