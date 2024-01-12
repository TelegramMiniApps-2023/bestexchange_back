# Generated by Django 4.2.7 on 2024-01-12 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangedirection',
            name='in_count',
            field=models.DecimalField(decimal_places=4, max_digits=10, verbose_name='Сколько отдаём'),
        ),
        migrations.AlterField(
            model_name='exchangedirection',
            name='out_count',
            field=models.DecimalField(decimal_places=4, max_digits=10, verbose_name='Сколько получаем'),
        ),
    ]
