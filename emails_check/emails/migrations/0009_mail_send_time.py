# Generated by Django 5.0.6 on 2024-06-10 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0008_rename_send_time_mail_raw_send_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='send_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
