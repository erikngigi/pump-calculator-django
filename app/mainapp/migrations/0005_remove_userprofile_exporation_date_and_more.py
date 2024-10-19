# Generated by Django 5.0.7 on 2024-10-18 15:25

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_userprofile_exporation_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='exporation_date',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 17, 15, 25, 1, 369255, tzinfo=datetime.timezone.utc)),
        ),
    ]
