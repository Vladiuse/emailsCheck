# Generated by Django 5.0.6 on 2024-06-10 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0007_remove_maillink_is_alien_alter_maillink_domain_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mail',
            old_name='send_time',
            new_name='raw_send_time',
        ),
    ]
