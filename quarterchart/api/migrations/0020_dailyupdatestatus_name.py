# Generated by Django 4.1.7 on 2023-02-21 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_alter_dailyupdatestatus_last_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyupdatestatus',
            name='name',
            field=models.CharField(default='mktcap', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
