# Generated by Django 2.2.dev20180914183443 on 2019-01-15 15:44

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, null=True, verbose_name='Nick')),
                ('steamid64', models.CharField(max_length=255, unique=True, verbose_name='Steamid 64')),
                ('steamid32', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Steamid 32')),
                ('email', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='E-mail')),
                ('avatar', models.CharField(blank=True, max_length=255, null=True, verbose_name='Avatar')),
                ('avatar_medium', models.CharField(blank=True, max_length=255, null=True, verbose_name='Avatar Medium')),
                ('avatar_full', models.CharField(blank=True, max_length=255, null=True, verbose_name='Avatar Full')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data dołączenia')),
                ('cash', models.DecimalField(decimal_places=2, default=0, max_digits=19, verbose_name='Pieniądze')),
                ('is_active', models.BooleanField(default=True, verbose_name='Jest aktywny?')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Jest adminem?')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
            ],
            options={
                'verbose_name': 'użytkownik',
                'verbose_name_plural': 'użytkownicy',
            },
        ),
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=50, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('USER', 'Przekaz dla użytkownika'), ('SHOP', 'Sklep'), ('SMS', 'SMS'), ('CODE', 'Kod promocyjny'), ('TRANSFER', 'Przelew')], default='SHOP', max_length=50)),
                ('target', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'PaymentHistory',
                'verbose_name_plural': 'PaymentHistorys',
            },
        ),
        migrations.CreateModel(
            name='MyGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='name')),
                ('login_format', models.CharField(blank=True, max_length=512, null=True)),
                ('permissions', models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='permissions')),
            ],
            options={
                'verbose_name': 'grupa',
                'verbose_name_plural': 'grupy',
            },
            managers=[
                ('objects', accounts.models.GroupManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='accounts.MyGroup', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
