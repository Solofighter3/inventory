# Generated by Django 4.2.1 on 2023-08-10 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_youritem_location'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Orders',
        ),
    ]
