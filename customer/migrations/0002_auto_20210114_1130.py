# Generated by Django 3.1.4 on 2021-01-14 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('cost', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_of_meat', to='customer.typeofmeat')),
            ],
        ),
        migrations.RenameModel(
            old_name='Tabeldailydate',
            new_name='Tabledailydate',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='meats',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='table',
        ),
        migrations.DeleteModel(
            name='Meats',
        ),
    ]
