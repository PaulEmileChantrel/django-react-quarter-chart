# Generated by Django 4.1.6 on 2023-02-10 23:46

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_companiebalancesheet_full_num_col_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='companieinfo',
            name='next_earnings_date',
            field=models.DateTimeField(blank=True, default=api.models.yesterday, null=True),
        ),
    ]
