# Generated by Django 4.1.6 on 2023-02-06 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_full_annual_cash_flow_statement_companiecashflow_full_annual_cash_flow_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companie',
            name='ticker',
            field=models.CharField(max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='companieinfo',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compagnie_info', to='api.companie'),
        ),
    ]
