from datetime import date

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# from simple_history.models import HistoricalRecords


class AbstractCertificationRecord(models.Model):
    """ implements base certification fields and methods
    """
    class Meta:
        abstract = True

    owner = models.OneToOneField("core.Profile", on_delete=models.PROTECT)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    # updated_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    # create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    issued_date = models.DateField(default=date.today)
    # issued_by = models.CharField(max_length=768)

    # signed_hash = models.CharField()
    # signing_key_id


class SportRanks(models.IntegerChoices):
    kyu_10 = 10, _("10th kyu")
    kyu_09 = 20, _("9th kyu")
    kyu_08 = 30, _("8th kyu")
    kyu_07 = 40, _("7th kyu")
    kyu_06 = 50, _("6th kyu")
    kyu_05 = 60, _("5th kyu")
    kyu_04 = 70, _("4th kyu")
    kyu_03 = 80, _("3rd kyu")
    kyu_02 = 90, _("2nd kyu")
    kyu_01 = 100, _("1st kyu")
    dan_01 = 1100, _("1st dan")
    dan_02 = 1200, _("2nd dan")
    dan_03 = 1300, _("3rd dan")
    dan_04 = 1400, _("4th dan")
    dan_05 = 1500, _("5th dan")
    dan_06 = 1600, _("6th dan")
    dan_07 = 1700, _("7th dan")
    dan_08 = 1800, _("8th dan")
    dan_09 = 1900, _("9th dan")
    dan_10 = 2000, _("10th dan")


class SportCertificationRecord(AbstractCertificationRecord):
    """ implements base certifications for sport disciplines
    """
    class Meta:
        verbose_name = _("sport certification record")
        verbose_name_plural = _("sport certification records")
        db_table = "certification_sport_record"

    level = models.SmallIntegerField(choices=SportRanks.choices, default=SportRanks.kyu_10, db_index=True)

    discipline = models.ForeignKey('chanbara.SportDiscipline', related_name='certs', on_delete=models.PROTECT)

    # history = HistoricalRecords()

    def __str__(self):
        return f"{self.owner.get_full_name()} - {self.discipline} {self.get_level_display()}"
