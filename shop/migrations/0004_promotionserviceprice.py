# Generated by Django 2.2.dev20180914183443 on 2019-03-09 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20190222_1845'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionServicePrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.CharField(max_length=36)),
                ('new_value', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Service')),
            ],
            options={
                'verbose_name': 'Sklep - Promocyjna cena',
                'verbose_name_plural': 'Sklep - Promocyjne ceny',
            },
        ),
    ]
