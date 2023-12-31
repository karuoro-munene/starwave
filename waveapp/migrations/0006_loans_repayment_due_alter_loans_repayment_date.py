# Generated by Django 4.2.3 on 2023-07-14 15:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waveapp', '0005_loans_default_status_alter_loans_repayment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='loans',
            name='repayment_due',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='loans',
            name='repayment_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 21, 15, 15, 32, 741325, tzinfo=datetime.timezone.utc)),
        ),
    ]
