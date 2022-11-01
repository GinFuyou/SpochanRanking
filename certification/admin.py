from django.contrib import admin

from certification.models import SportCertificationRecord

# from simple_history.admin import SimpleHistoryAdmin


@admin.register(SportCertificationRecord)
# class SportCertAdmin(SimpleHistoryAdmin):
class SportCertAdmin(admin.ModelAdmin):
    pass
