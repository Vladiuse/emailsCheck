# Generated by Django 5.0.6 on 2024-06-10 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0005_alter_mail_send_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_html_link', models.CharField(blank=True, max_length=255)),
                ('link', models.CharField(blank=True, max_length=255)),
                ('domain', models.CharField(blank=True, max_length=255)),
                ('is_alien', models.BooleanField(blank=True, null=True)),
                ('mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emails.mail')),
            ],
        ),
    ]
