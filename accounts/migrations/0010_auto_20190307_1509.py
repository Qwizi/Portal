# Generated by Django 2.2.dev20180914183443 on 2019-03-07 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20190307_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mygroup',
            name='login_format',
            field=models.CharField(default='{username}', max_length=512),
        ),
    ]