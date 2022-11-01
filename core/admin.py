# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# from simple_history.admin import SimpleHistoryAdmin
from .models import Profile


@admin.register(get_user_model())
class CoreUserAdmin(UserAdmin):
    list_display = ['admin_display_name', 'email', 'is_staff', 'is_active', 'date_joined']
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    ("is_staff", "is_superuser"),
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(Profile)
# class ProfileAdmin(SimpleHistoryAdmin):
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'last_name', 'first_name', 'date_of_birth']
