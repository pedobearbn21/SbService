# Generated by Django 3.1.4 on 2021-01-30 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_meat_meat_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablestableinstore',
            name='status',
            field=models.CharField(choices=[('OPEN', 'OPEN'), ('CLOSE', 'CLOSE')], default='OPEN', max_length=5),
        ),
    ]
