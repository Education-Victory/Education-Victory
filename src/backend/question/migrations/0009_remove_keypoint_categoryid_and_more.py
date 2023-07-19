# Generated by Django 4.1.4 on 2023-07-06 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_remove_user_ability_id_remove_usersubmission_details_and_more'),
        ('question', '0008_rename_category_keypoint_categoryid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keypoint',
            name='categoryId',
        ),
        migrations.RemoveField(
            model_name='userkeypointscore',
            name='keypoint',
        ),
        migrations.RemoveField(
            model_name='userkeypointscore',
            name='user',
        ),
        migrations.RemoveField(
            model_name='question',
            name='type',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='ability_id',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='keypoint',
        ),
        migrations.AddField(
            model_name='question',
            name='ide_description',
            field=models.JSONField(blank=True, default={'data': ''}, help_text='default description/code in the IDE'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solution',
            name='ability',
            field=models.JSONField(default={'data': ''}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solution',
            name='type',
            field=models.CharField(choices=[('CO', 'Coding'), ('CH', 'Choice')], default='CO', help_text='solution type', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='category of question/solution', max_length=30),
        ),
        migrations.AlterField(
            model_name='category',
            name='weight',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='question',
            name='URL',
            field=models.URLField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='question',
            name='category_id_list',
            field=models.ManyToManyField(help_text='category list related to question based on its solution', to='question.category'),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='downvote',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='question',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='question',
            name='upvote',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='solution',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Ability',
        ),
        migrations.DeleteModel(
            name='Keypoint',
        ),
        migrations.DeleteModel(
            name='UserKeypointScore',
        ),
    ]
