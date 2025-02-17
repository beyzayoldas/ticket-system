# Generated by Django 5.0.7 on 2024-08-26 11:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0019_alter_response_time_spent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_responses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='response',
            name='status',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='response',
            name='time_spent',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
