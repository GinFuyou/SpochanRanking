# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


@admin.register(get_user_model())
class CoreUserAdmin(UserAdmin):
    list_display = ['admin_display_name', 'email', 'is_staff', 'is_active', 'date_joined']
