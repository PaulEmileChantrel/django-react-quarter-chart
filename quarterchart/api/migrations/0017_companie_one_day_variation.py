# Generated by Django 4.1.7 on 2023-02-19 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_companie_share_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='companie',
            name='one_day_variation',
            field=models.FloatField(default=0),
        ),
    ]