# Generated by Django 5.0.7 on 2024-10-18 15:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='exporation_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 17, 15, 21, 5, 314638, tzinfo=datetime.timezone.utc)),
        ),
    ]
