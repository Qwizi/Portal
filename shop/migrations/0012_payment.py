# Generated by Django 2.2.dev20180914183443 on 2019-03-20 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20190310_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tag', models.CharField(max_length=36)),
            ],
            options={
                'verbose_name': 'Sklep - Płatność',
                'verbose_name_plural': 'Sklep - Płatnosci',
            },
        ),
    ]
