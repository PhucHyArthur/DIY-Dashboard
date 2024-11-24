# Generated by Django 5.1.3 on 2024-11-24 08:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('avatar', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(max_length=255)),
                ('birth', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('tel', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('bank_name', models.CharField(max_length=255)),
                ('bank_branch', models.CharField(max_length=255)),
                ('bank_number', models.CharField(max_length=50)),
                ('swift_code', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('avatar', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('tel', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=255)),
                ('tax_code', models.CharField(max_length=50)),
                ('bank_name', models.CharField(max_length=255)),
                ('bank_branch', models.CharField(max_length=255)),
                ('bank_number', models.CharField(max_length=50)),
                ('swift_code', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('representative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suppliers', to='suppliers.representative')),
            ],
        ),
    ]
