from django.contrib import admin

from chanbara import models


# Register your models here.
@admin.register(models.SportDiscipline)
class SportDisciplineAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}


@admin.register(models.GroupType)
class GroupTypeAdmin(admin.ModelAdmin):
    list_display = (str, 'is_primary', 'is_junior')
