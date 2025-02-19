# Generated by Django 5.1.6 on 2025-02-19 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('design', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programmed_quantity', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='design.design')),
            ],
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.person')),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField()),
                ('start_date', models.DateTimeField()),
                ('expected_delivery_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.batch')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.process')),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.workshop')),
            ],
        ),
    ]
