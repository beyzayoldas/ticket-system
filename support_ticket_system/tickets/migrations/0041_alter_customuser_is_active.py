# Generated by Django 5.0.7 on 2025-01-03 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0040_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
