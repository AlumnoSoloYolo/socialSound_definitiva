# Generated by Django 5.1.1 on 2024-12-12 01:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialSound', '0005_alter_detallescancion_duracion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallescancion',
            name='duracion',
            field=models.DurationField(default=datetime.timedelta),
        ),
    ]
