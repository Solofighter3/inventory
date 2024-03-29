# Generated by Django 4.2.1 on 2023-08-12 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.IntegerField(unique=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.orders')),
            ],
        ),
    ]
