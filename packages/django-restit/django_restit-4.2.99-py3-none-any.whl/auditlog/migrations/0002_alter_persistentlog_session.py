# Generated by Django 4.2.11 on 2024-05-13 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessionlog', '0001_initial'),
        ('auditlog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persistentlog',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sessionlog.sessionlog'),
        ),
    ]
