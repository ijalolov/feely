from django.contrib import admin
from .models import *


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    filter_horizontal = ('specializations',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass


@admin.register(VideoCourse)
class VideoCourseAdmin(admin.ModelAdmin):
    pass


@admin.register(VideoCourseCategory)
class VideoCourseCategoryAdmin(admin.ModelAdmin):
    pass
