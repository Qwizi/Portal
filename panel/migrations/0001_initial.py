# Generated by Django 2.2.dev20180914183443 on 2019-01-15 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('servers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tag', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('servers', models.ManyToManyField(to='servers.Server')),
            ],
            options={
                'verbose_name': 'Modules',
                'verbose_name_plural': 'Moduless',
            },
        ),
    ]