# Generated by Django 3.1.4 on 2021-01-14 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20210114_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='meats',
            field=models.ManyToManyField(to='customer.Meat'),
        ),
    ]