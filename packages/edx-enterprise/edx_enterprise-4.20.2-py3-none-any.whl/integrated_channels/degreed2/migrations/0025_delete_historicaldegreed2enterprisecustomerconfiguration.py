# Generated by Django 3.2.19 on 2024-02-20 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('degreed2', '0024_degreed2learnerdatatransmissionaudit_degreed2_unique_enrollment_course_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistoricalDegreed2EnterpriseCustomerConfiguration',
        ),
    ]
