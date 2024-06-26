# Generated by Django 5.0.4 on 2024-05-14 21:41

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_api', '0003_alter_account_status_valid_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='guid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
