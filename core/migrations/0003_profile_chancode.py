# Generated by Django 4.2.5 on 2023-10-12 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_data_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='chancode',
            field=models.CharField(blank=True, max_length=16, null=True, unique=True),
        ),
    ]