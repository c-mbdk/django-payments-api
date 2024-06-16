# Generated by Django 5.0.4 on 2024-05-08 09:59

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=19)),
                ('currency', models.CharField(max_length=3)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('credit_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts_api.account')),
                ('debit_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts_api.account')),
            ],
        ),
    ]
