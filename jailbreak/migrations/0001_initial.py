# Generated by Django 2.2.dev20180914183443 on 2019-01-19 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Custom_ChatColors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identity', models.CharField(max_length=32, unique=True)),
                ('flag', models.CharField(blank=True, max_length=1, null=True)),
                ('tag', models.CharField(max_length=32)),
                ('tagcolor', models.CharField(blank=True, max_length=8, null=True)),
                ('namecolor', models.CharField(blank=True, max_length=8, null=True)),
                ('textcolor', models.CharField(blank=True, max_length=8, null=True)),
                ('alias', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Custom_ChatColors',
                'verbose_name_plural': 'Custom_ChatColors',
            },
        ),
        migrations.CreateModel(
            name='Sm_Admins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authtype', models.CharField(choices=[('STEAM', 'steam'), ('NAME', 'name'), ('IP', 'ip')], default='STEAM', max_length=50)),
                ('identity', models.CharField(max_length=65)),
                ('password', models.CharField(blank=True, max_length=65, null=True)),
                ('flags', models.CharField(blank=True, max_length=30, null=True)),
                ('name', models.CharField(max_length=65)),
                ('immunity', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Admin SourceMod',
                'verbose_name_plural': 'Admini SourceMod',
            },
        ),
        migrations.CreateModel(
            name='Sm_Groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flags', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=120)),
                ('immunity_level', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Grupa SourceMod',
                'verbose_name_plural': 'Grupy SourceMod',
            },
        ),
        migrations.CreateModel(
            name='Sm_Overrides',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('command', 'command'), ('group', 'group')], default='command', max_length=50)),
                ('name', models.CharField(max_length=32)),
                ('flags', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'ModelName',
                'verbose_name_plural': 'ModelNames',
            },
        ),
        migrations.CreateModel(
            name='Store_Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.IntegerField()),
                ('type', models.CharField(max_length=16)),
                ('unique_id', models.CharField(max_length=256)),
                ('slot', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Store_Equipment',
                'verbose_name_plural': 'Store_Equipments',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Store_Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.IntegerField()),
                ('type', models.CharField(max_length=16)),
                ('unique_id', models.CharField(max_length=256)),
                ('date_of_purchase', models.DateField()),
                ('date_of_expiration', models.DateField()),
                ('price_of_purchase', models.IntegerField()),
            ],
            options={
                'verbose_name': 'StoreItems',
                'verbose_name_plural': 'StoreItemss',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Store_Players',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authid', models.CharField(max_length=32, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('credits', models.BigIntegerField()),
                ('date_of_join', models.DateField()),
                ('date_of_last_join', models.DateField()),
            ],
            options={
                'verbose_name': 'store_players',
                'verbose_name_plural': 'store_playerss',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Sm_GroupOverrides',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('command', 'command'), ('group', 'group')], default='command', max_length=50)),
                ('name', models.CharField(max_length=32)),
                ('access', models.CharField(choices=[('allow', 'allow'), ('deny', 'deny')], default='allow', max_length=50)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jailbreak.Sm_Groups')),
            ],
            options={
                'verbose_name': 'Sm_GroupOver',
                'verbose_name_plural': 'Sm_GroupOvers',
                'db_table': 'jailbreak_sm_group_overrides',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Sm_GroupImmunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_id', models.PositiveIntegerField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jailbreak.Sm_Groups')),
            ],
            options={
                'verbose_name': 'Immunitet Grupy SourceMod',
                'verbose_name_plural': 'Immunitety Grup SourceMod',
                'db_table': 'jailbreak_sm_group_immunity',
            },
        ),
    ]
