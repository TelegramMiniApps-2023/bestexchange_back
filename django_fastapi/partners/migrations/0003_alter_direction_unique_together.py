# Generated by Django 4.2.7 on 2024-02-19 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0001_initial'),
        ('partners', '0002_alter_partnercity_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='direction',
            unique_together={('city', 'direction')},
        ),
    ]