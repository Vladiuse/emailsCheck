# Generated by Django 5.0.6 on 2024-06-09 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='emails_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
