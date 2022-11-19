from django.contrib import admin

from psy_test.models import TestOption, Test


class TestOptionInline(admin.TabularInline):
    model = TestOption
    extra = 0


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [TestOptionInline]
    list_display = ('question', 'order')
    list_editable = ['order']
