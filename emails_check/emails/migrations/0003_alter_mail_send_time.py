# Generated by Django 5.0.6 on 2024-06-09 20:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_alter_email_emails_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='send_time',
            field=models.DateField(default=datetime.datetime(2024, 6, 9, 20, 54, 16, 992004)),
        ),
    ]
