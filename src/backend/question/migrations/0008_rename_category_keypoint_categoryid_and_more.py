# Generated by Django 4.1.4 on 2023-06-28 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0007_ability_solution_difficulty'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keypoint',
            old_name='category',
            new_name='categoryId',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='category',
            new_name='category_id_list',
        ),
        migrations.RenameField(
            model_name='solution',
            old_name='difficulty',
            new_name='ability_id',
        ),
        migrations.RenameField(
            model_name='solution',
            old_name='question',
            new_name='question_id',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='category',
        ),
        migrations.AddField(
            model_name='solution',
            name='category_id_list',
            field=models.ManyToManyField(to='question.category'),
        ),
        migrations.DeleteModel(
            name='UserSubmission',
        ),
    ]
