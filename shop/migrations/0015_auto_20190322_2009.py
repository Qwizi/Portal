# Generated by Django 2.2.dev20180914183443 on 2019-03-22 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20190320_1723'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bonus',
            options={'verbose_name': 'Sklep - Bonus', 'verbose_name_plural': 'Sklep - Bonusy'},
        ),
        migrations.AlterModelOptions(
            name='premium',
            options={'verbose_name': 'Sklep - Premka', 'verbose_name_plural': 'Sklep - Premki'},
        ),
        migrations.AlterModelOptions(
            name='premiumcache',
            options={'verbose_name': 'Sklep - Premka Cache', 'verbose_name_plural': 'Sklep - Premki Cache'},
        ),
        migrations.AlterModelOptions(
            name='price',
            options={'verbose_name': 'Sklep - Cena', 'verbose_name_plural': 'Sklep - Ceny'},
        ),
        migrations.AlterModelOptions(
            name='promotioncode',
            options={'verbose_name': 'Sklep - Kod promocyjny', 'verbose_name_plural': 'Sklep - Kody promocyjne'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'Sklep - Usluga', 'verbose_name_plural': 'Sklep - Uslugi'},
        ),
        migrations.AlterModelOptions(
            name='smsnumber',
            options={'verbose_name': 'Sklep - Numer SMS', 'verbose_name_plural': 'Sklep - Numery SMS'},
        ),
    ]
