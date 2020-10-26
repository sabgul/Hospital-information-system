# Generated by Django 3.1.2 on 2020-10-26 10:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitalis', '0003_auto_20201026_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='date_of_birth',
            field=models.DateField(default=datetime.date.today, max_length=8),
        ),
        migrations.AlterField(
            model_name='healthcareworker',
            name='date_of_birth',
            field=models.DateField(default=datetime.date.today, max_length=8),
        ),
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(default=datetime.date.today, max_length=8),
        ),
    ]
