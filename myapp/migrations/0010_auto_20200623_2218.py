# Generated by Django 3.0.7 on 2020-06-24 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20200623_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='levels',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[(0, 'Cancelled'), (1, 'Order Confirmed')], default='Order Confirmed', max_length=100, null=True),
        ),
    ]
