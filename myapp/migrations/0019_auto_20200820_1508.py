# Generated by Django 3.0.8 on 2020-08-20 19:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_auto_20200721_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='hours',
            field=models.DecimalField(decimal_places=2, default=40.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.date(2020, 8, 20)),
        ),
    ]
