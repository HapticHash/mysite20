# Generated by Django 3.0.7 on 2020-06-24 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_auto_20200623_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[(0, 'Cancelled'), (1, 'Order Confirmed')], default=1, max_length=2, null=True),
        ),
    ]
