# Generated by Django 4.2.7 on 2024-01-12 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0002_alter_exchangedirection_in_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangedirection',
            name='in_count',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сколько отдаём'),
        ),
        migrations.AlterField(
            model_name='exchangedirection',
            name='out_count',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сколько получаем'),
        ),
    ]
