# Generated by Django 5.1.1 on 2024-10-04 12:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskentrymodel",
            name="estimated_time",
            field=models.DurationField(default="1:00:00"),
        ),
        migrations.AlterField(
            model_name="taskentrymodel",
            name="execution_time",
            field=models.DurationField(default="0:00:00"),
        ),
    ]
