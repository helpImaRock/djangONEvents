# Generated by Django 3.1.6 on 2021-02-28 00:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='event',
            name='date_gte_present',
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='date'),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.CheckConstraint(check=models.Q(date__gte=datetime.date(2021, 2, 28)), name='date_gte_present'),
        ),
    ]