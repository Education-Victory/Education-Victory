# Generated by Django 4.1.4 on 2024-06-21 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0009_alter_problem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemfrequency',
            name='position_type',
            field=models.CharField(choices=[('Software Engineer', 'Software Engineer'), ('Frontend Engineer', 'Frontend Engineer'), ('Machine Learning', 'Machine Learning'), ('Data Scientist', 'Data Scientist')], default='Software Engineer', max_length=20),
        ),
        migrations.AlterField(
            model_name='problemfrequency',
            name='stage',
            field=models.CharField(choices=[('Phone', 'Phone'), ('Onsite', 'Onsite')], default='Onsite', max_length=20),
        ),
    ]