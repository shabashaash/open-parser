# Generated by Django 3.0.4 on 2020-03-29 22:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoostModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Bmodel', models.BinaryField()),
                ('label', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Labels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('label', models.IntegerField()),
                ('used', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ToParse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(max_length=255)),
                ('tag', models.CharField(max_length=255)),
                ('ptag', models.CharField(max_length=255)),
                ('pptag', models.CharField(max_length=255)),
                ('Cclass', models.CharField(max_length=255)),
                ('pclass', models.CharField(max_length=255)),
                ('ppclass', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Zeros',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('true_label', models.IntegerField()),
                ('data', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('used', models.BooleanField(default=False)),
            ],
        ),
    ]