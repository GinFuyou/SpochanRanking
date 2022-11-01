from django.contrib import admin

from certification.models import SportCertificationRecord


# Register your models here.
@admin.register(SportCertificationRecord)
class SportCertAdmin(admin.ModelAdmin):
    pass
