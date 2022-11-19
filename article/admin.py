from django.contrib import admin
from django.urls import path, include
from .models import Article, Adv, AdvImage


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


class AdvImageInline(admin.TabularInline):
    model = AdvImage
    extra = 0


@admin.register(Adv)
class AdvAdmin(admin.ModelAdmin):
    inlines = [AdvImageInline]

    def get_queryset(self, request):
        Adv.get_solo()
        return super().get_queryset(request)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
