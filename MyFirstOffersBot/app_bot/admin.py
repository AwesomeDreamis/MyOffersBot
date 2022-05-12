from django.contrib import admin
from .models import Employer


@admin.register(Employer)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'tg_chat_id', 'sent']
