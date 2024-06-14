# Generated by Django 4.1.4 on 2024-02-23 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0004_remove_address_modified_by_address_group_and_more'),
        ('account', '0018_userpasskey'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='location',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='location.address'),
        ),
    ]
