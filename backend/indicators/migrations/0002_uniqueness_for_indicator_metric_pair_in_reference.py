# Generated by Django 3.2.18 on 2023-09-18 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='indicator_metric_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='indicators.indicatormetric', unique=True),
        ),
    ]
