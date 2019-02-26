# Generated by Django 2.2.dev20180914183443 on 2019-01-16 18:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0002_server_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='managers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]