# Generated by Django 4.2.7 on 2023-12-19 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0002_blacklistelement_cash_blackl_city_4c3c37_idx_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='city',
            index=models.Index(fields=['code_name'], name='cash_city_code_na_f76bcc_idx'),
        ),
    ]