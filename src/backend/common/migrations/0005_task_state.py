# Generated by Django 4.1.4 on 2023-08-30 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_alter_user_ability'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='state',
            field=models.CharField(default='New', max_length=100),
        ),
    ]