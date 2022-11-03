# from django.conf import settings
from django.db import models

# from django.utils.translation import gettext_lazy as _


class SportDiscipline(models.Model):
    """ implements sport disciplines like weapon categories and kihon-dosa
    """
    class Meta:
        pass

    id = models.SmallAutoField(primary_key=True)  # don't use BigAutoField where it's not needed

    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
    is_certifiable = models.BooleanField(default=False)

    priority = models.SmallIntegerField(default=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Competition(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=512)
    slug = models.SlugField(max_length=256, unique=True)
    scale = models.DecimalField(max_digits=9, decimal_places=4)

    date = models.DateField()
    # location = ?


class CompGroup(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('competition', 'name'), name='unique_group_name_for_competition'),
        ]

    competition = models.ForeignKey('Competition')
    name = models.CharField(max_length=256)
    # grand_champion = models.ForeignKey(....)


"""
class CompGroupDiscipline(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('group', 'discipline'), name='unique_discipline_for_group'),
        ]

    group = models.ForeignKey("CompGroup")
    discipline = models.ForeignKey("SportDiscipline")
    # place1 = models.ForeignKey(....)
    # place2 = models.ForeignKey(....)
    # place3 = models.ForeignKey(....)
    # place4 = models.ForeignKey(....)
"""
