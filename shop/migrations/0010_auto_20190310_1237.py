# Generated by Django 2.2.dev20180914183443 on 2019-03-10 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20190310_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotionserviceprice',
            name='percent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
    ]
