# Generated by Django 2.2.dev20180914183443 on 2019-01-20 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jailbreak', '0005_auto_20190120_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sm_admins',
            name='groups',
            field=models.ManyToManyField(blank=True, to='jailbreak.Sm_Groups'),
        ),
    ]