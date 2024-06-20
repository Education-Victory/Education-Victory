# Generated by Django 4.1.4 on 2024-06-20 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0008_rename_job_category_problemfrequency_position_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='category',
            field=models.CharField(choices=[('Algorithm', 'Algorithm'), ('System Design', 'System Design'), ('Computer Science', 'Computer Science'), ('Behavioral', 'Behavioral'), ('Resume', 'Resume')], default='Algorithm', max_length=100),
        ),
    ]