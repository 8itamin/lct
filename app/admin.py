from django.contrib import admin
from .models import *


@admin.register(Books)
class Books(admin.ModelAdmin):
    list_display = ['id_book','title', 'author']
    search_fields = ['id_book']

@admin.register(Recomendations)
class Books(admin.ModelAdmin):
    list_display = ['id_client','req_1', 'req_2', 'req_3', 'req_4', 'req_5']
    search_fields = ['id_client']

@admin.register(History)
class History(admin.ModelAdmin):
    list_display = ['id_client','id_book', 'start_read', 'finish_read']
    search_fields = ['id_client']