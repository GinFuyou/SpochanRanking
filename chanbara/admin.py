from django.contrib import admin

from chanbara.models import SportDiscipline


# Register your models here.
@admin.register(SportDiscipline)
class SportDisciplineAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}
