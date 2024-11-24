# Generated by Django 5.1.3 on 2024-11-24 08:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aisle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('capacity', models.IntegerField(default=0)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_fulled', models.BooleanField(default=False, verbose_name='Is Fulled')),
            ],
            options={
                'verbose_name': 'Aisle',
                'verbose_name_plural': 'Aisles',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('capacity', models.IntegerField(default=0)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_fulled', models.BooleanField(default=False, verbose_name='Is Fulled')),
            ],
            options={
                'verbose_name': 'Warehouse',
                'verbose_name_plural': 'Warehouses',
            },
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('capacity', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_fulled', models.BooleanField(default=False, verbose_name='Is Fulled')),
                ('aisle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='racks', to='warehouse.aisle')),
            ],
            options={
                'verbose_name': 'Rack',
                'verbose_name_plural': 'Racks',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bin_number', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_fulled', models.BooleanField(default=False, verbose_name='Is Fulled')),
                ('rack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='warehouse.rack')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('capacity', models.IntegerField(default=0)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_fulled', models.BooleanField(default=False, verbose_name='Is Fulled')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zones', to='warehouse.warehouse')),
            ],
            options={
                'verbose_name': 'Zone',
                'verbose_name_plural': 'Zones',
            },
        ),
        migrations.AddField(
            model_name='aisle',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aisles', to='warehouse.zone'),
        ),
    ]
