# Generated by Django 5.2.1 on 2025-05-16 05:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], db_index=True, max_length=20),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['status'], name='core_task_status_e18e62_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['priority'], name='core_task_priorit_e802be_idx'),
        ),
    ]
