# Generated by Django 3.1.4 on 2021-03-13 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_auto_20210313_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderreciept',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meat_to_order', to='customer.orders'),
        ),
    ]