# Generated by Django 4.1.4 on 2024-02-20 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_geoip_subnet_alter_geoip_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='postalcode_suffix',
            field=models.CharField(blank=True, default=None, max_length=32, null=True),
        ),
    ]
