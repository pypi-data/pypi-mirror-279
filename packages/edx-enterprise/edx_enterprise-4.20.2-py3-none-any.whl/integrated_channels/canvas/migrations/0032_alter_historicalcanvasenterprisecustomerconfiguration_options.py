# Generated by Django 3.2.20 on 2023-08-08 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('canvas', '0031_auto_20230719_1621'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalcanvasenterprisecustomerconfiguration',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical canvas enterprise customer configuration', 'verbose_name_plural': 'historical canvas enterprise customer configurations'},
        ),
    ]
