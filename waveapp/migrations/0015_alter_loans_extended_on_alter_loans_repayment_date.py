# Generated by Django 4.2.3 on 2023-07-26 08:07

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('waveapp', '0014_loans_extended_on_alter_loans_repayment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loans',
            name='extended_on',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DateTimeField(default=django.utils.timezone.now), blank=True, default=[], size=None),
        ),
        migrations.AlterField(
            model_name='loans',
            name='repayment_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 2, 8, 7, 35, 422384, tzinfo=datetime.timezone.utc)),
        ),
    ]
