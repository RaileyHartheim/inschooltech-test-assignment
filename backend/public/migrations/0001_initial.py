# Generated by Django 3.2.18 on 2023-09-17 08:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=255, verbose_name="laboratory's name")),
            ],
            options={
                'verbose_name': 'lab',
                'verbose_name_plural': 'labs',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('started_at', models.DateTimeField(verbose_name='test started at')),
                ('completed_at', models.DateTimeField(verbose_name='test completed at')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='comment for test')),
                ('lab_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='public.lab', verbose_name='lab where test was taken')),
            ],
            options={
                'verbose_name': 'test',
                'verbose_name_plural': 'tests',
                'ordering': ('-created_at',),
            },
        ),
    ]