from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'login',
        'name',
        'date_joined',
        'status',
        'search_history',
        'visit_history',
        'phone_number'
    )
