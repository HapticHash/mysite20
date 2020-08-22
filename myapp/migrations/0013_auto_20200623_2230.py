# Generated by Django 3.0.7 on 2020-06-24 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_order_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('0', 'Cancelled'), ('1', 'Order Confirmed')], default='1', max_length=100, null=True),
        ),
    ]