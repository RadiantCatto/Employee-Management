# Generated by Django 3.2.13 on 2023-04-11 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employees', '0005_alter_workschedules_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workschedules',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employees.employees'),
        ),
    ]