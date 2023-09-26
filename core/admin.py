# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

# from simple_history.admin import SimpleHistoryAdmin
from .models import Profile, SportClub


class CoreUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email', )


@admin.register(get_user_model())
class CoreUserAdmin(UserAdmin):
    add_form = CoreUserCreationForm

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

    search_fields = ('username', 'email')

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            form_class = self.add_form
        else:
            form_class = super().get_form(request, obj, **defaults)
        return form_class


@admin.register(Profile)
# class ProfileAdmin(SimpleHistoryAdmin):
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'last_name', 'first_name', 'date_of_birth']
    readonly_fields = ("html_profile_qr", )
    fields = ('first_name', 'last_name', 'date_of_birth', 'html_profile_qr')
    autocomplete_fields = ('club', 'owner')
    search_fields = ('first_name', 'last_name', 'middle_name', 'owner__email')


@admin.register(SportClub)
class SportClubAdmin(admin.ModelAdmin):
    list_display = (str, 'location')
    search_fields = ('name', 'location')
