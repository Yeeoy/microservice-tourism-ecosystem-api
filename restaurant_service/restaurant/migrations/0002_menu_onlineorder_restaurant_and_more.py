# Generated by Django 5.1 on 2024-10-16 12:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='OnlineOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('order_date', models.DateField()),
                ('order_time', models.TimeField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_status', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('cuisine_type', models.CharField(max_length=255)),
                ('opening_hours', models.CharField(max_length=255)),
                ('contact_info', models.CharField(max_length=255)),
                ('img_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='routeplanning',
            name='provider_id',
        ),
        migrations.RemoveField(
            model_name='trafficupdate',
            name='provider_id',
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.menu')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='restaurant.onlineorder')),
            ],
        ),
        migrations.AddField(
            model_name='onlineorder',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
        migrations.AddField(
            model_name='menu',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
        migrations.CreateModel(
            name='TableReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('reservation_date', models.DateField()),
                ('reservation_time', models.TimeField()),
                ('number_of_guests', models.PositiveIntegerField()),
                ('reservation_status', models.CharField(max_length=255)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant')),
            ],
        ),
        migrations.DeleteModel(
            name='RideBooking',
        ),
        migrations.DeleteModel(
            name='RoutePlanning',
        ),
        migrations.DeleteModel(
            name='TrafficUpdate',
        ),
        migrations.DeleteModel(
            name='TransportationProvider',
        ),
    ]
