# Generated by Django 2.2.dev20180914183443 on 2019-03-20 17:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_payment_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotioncode',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
