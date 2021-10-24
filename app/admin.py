from django.contrib import admin
from .models import *


admin.site.register(Recomendations)

@admin.register(Books)
class Books(admin.ModelAdmin):
    list_display = ['id_book','title', 'author']
    search_fields = ['id_book']
