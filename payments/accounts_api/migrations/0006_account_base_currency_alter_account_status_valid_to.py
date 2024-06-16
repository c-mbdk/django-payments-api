# Generated by Django 5.0.4 on 2024-05-29 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_api', '0005_rename_guid_account_account_guid'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='base_currency',
            field=models.CharField(default='GBP', max_length=3),
        ),
        migrations.AlterField(
            model_name='account',
            name='status_valid_to',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
