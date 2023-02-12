from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date_joined',
        'status',
        'visit_time',
        'phone_number'
    )
