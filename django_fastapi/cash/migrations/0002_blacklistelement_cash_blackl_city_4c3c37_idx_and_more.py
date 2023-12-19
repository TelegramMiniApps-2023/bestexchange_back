# Generated by Django 4.2.7 on 2023-12-18 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='blacklistelement',
            index=models.Index(fields=['city', 'valute_from', 'valute_to'], name='cash_blackl_city_4c3c37_idx'),
        ),
        migrations.AddIndex(
            model_name='direction',
            index=models.Index(fields=['valute_from', 'valute_to'], name='cash_direct_valute__7db9f5_idx'),
        ),
        migrations.AddIndex(
            model_name='exchangedirection',
            index=models.Index(fields=['city', 'valute_from', 'valute_to'], name='cash_exchan_city_643452_idx'),
        ),
    ]
