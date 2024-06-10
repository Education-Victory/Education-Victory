# Generated by Django 4.1.4 on 2024-05-21 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0004_alter_problemfrequency_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemfrequency',
            name='job_category',
            field=models.CharField(choices=[('oa', 'OA'), ('phone', 'Phone'), ('onsite', 'Onsite')], default='swe', max_length=20),
        ),
        migrations.AddField(
            model_name='problemfrequency',
            name='origin_content',
            field=models.CharField(blank=True, max_length=4000),
        ),
    ]