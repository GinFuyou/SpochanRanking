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
