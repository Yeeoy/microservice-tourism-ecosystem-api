# Generated by Django 5.1 on 2024-10-16 09:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('star_rating', models.PositiveIntegerField()),
                ('total_rooms', models.PositiveIntegerField()),
                ('amenities', models.TextField()),
                ('check_in_time', models.TimeField()),
                ('check_out_time', models.TimeField()),
                ('contact_info', models.CharField(max_length=255)),
                ('img_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(max_length=255)),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_occupancy', models.PositiveIntegerField()),
                ('availability', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('rating', models.PositiveIntegerField()),
                ('review', models.TextField()),
                ('date', models.DateField()),
                ('accommodation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodation.accommodation')),
            ],
        ),
        migrations.CreateModel(
            name='GuestService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('availability_hours', models.CharField(max_length=255)),
                ('accommodation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodation.accommodation')),
            ],
        ),
        migrations.CreateModel(
            name='RoomBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('booking_status', models.BooleanField(default=False)),
                ('payment_status', models.BooleanField(default=False)),
                ('accommodation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodation.accommodation')),
                ('room_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodation.roomtype')),
            ],
        ),
        migrations.AddField(
            model_name='accommodation',
            name='types',
            field=models.ManyToManyField(to='accommodation.roomtype'),
        ),
    ]
