# Generated by Django 2.2.dev20180914183443 on 2019-03-10 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20190310_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotionserviceprice',
            name='percent',
            field=models.FloatField(default=0.0),
        ),
    ]