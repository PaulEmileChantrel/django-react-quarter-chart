# Generated by Django 4.1.7 on 2023-02-21 20:44

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_companie_one_day_variation'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyUpdateStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated_at', models.DateTimeField(default=api.models.yesterday)),
            ],
        ),
    ]
