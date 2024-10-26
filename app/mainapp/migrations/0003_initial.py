# Generated by Django 5.0.7 on 2024-10-18 15:06

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainapp', '0002_remove_portfolio_user_remove_profile_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exporation_date', models.DateTimeField(default=datetime.datetime(2024, 11, 17, 15, 6, 23, 202626, tzinfo=datetime.timezone.utc))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]