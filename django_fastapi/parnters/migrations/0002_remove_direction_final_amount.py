# Generated by Django 4.2.7 on 2024-02-01 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parnters', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='direction',
            name='final_amount',
        ),
    ]