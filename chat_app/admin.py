from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'sender', 'receiver', 'date_time',)
    list_filter = ('sender', 'receiver', 'date_time',)
    search_fields = ('text', 'sender__username', 'receiver__username')
