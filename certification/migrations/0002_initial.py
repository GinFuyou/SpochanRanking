# Generated by Django 4.1.2 on 2022-11-01 13:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certification', '0001_initial'),
        ('core', '0001_initial'),
        ('chanbara', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportcertificationrecord',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sportcertificationrecord',
            name='discipline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='certs', to='chanbara.sportdiscipline'),
        ),
        migrations.AddField(
            model_name='sportcertificationrecord',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='core.profile'),
        ),
    ]
