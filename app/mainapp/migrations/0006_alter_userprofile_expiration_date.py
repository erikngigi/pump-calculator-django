# Generated by Django 5.0.7 on 2024-10-18 15:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_remove_userprofile_exporation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 17, 15, 29, 3, 811080, tzinfo=datetime.timezone.utc)),
        ),
    ]
