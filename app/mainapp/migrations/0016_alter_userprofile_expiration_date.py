# Generated by Django 5.0.7 on 2024-10-18 18:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_alter_userprofile_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 17, 18, 14, 59, 870388, tzinfo=datetime.timezone.utc)),
        ),
    ]
