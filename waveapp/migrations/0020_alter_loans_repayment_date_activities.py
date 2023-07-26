# Generated by Django 4.2.3 on 2023-07-26 08:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('waveapp', '0019_alter_loans_extended_on_alter_loans_repayment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loans',
            name='repayment_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 2, 8, 46, 12, 795470, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('New Loan', 'New Loan'), ('Loan Repayment', 'Loan Repayment'), ('Loan Extension', 'Loan Extension'), ('Loan Defaulted', 'Loan Defaulted')], max_length=100)),
                ('initiated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waveapp.loans')),
            ],
        ),
    ]
