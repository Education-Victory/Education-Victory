# Generated by Django 4.1.4 on 2024-03-19 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_alter_question_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='group',
            field=models.CharField(default='data-structure', max_length=100),
        ),
    ]
