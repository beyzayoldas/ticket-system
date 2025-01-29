# Generated by Django 5.0.7 on 2024-09-05 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0035_alter_kullanici_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kullanici',
            name='role',
            field=models.CharField(choices=[('ENDUSER', 'End User'), ('ITMANAGER', 'IT Manager'), ('OTHERMANAGER', 'Other Manager'), ('ITSTAFF', 'IT Staff')], default='ENDUSER', max_length=20),
        ),
    ]
