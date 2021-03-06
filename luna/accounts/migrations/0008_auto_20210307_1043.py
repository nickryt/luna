# Generated by Django 3.1.6 on 2021-03-07 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210307_1036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='username',
            new_name='user',
        ),
        migrations.AddField(
            model_name='account',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='img'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='vote',
            field=models.CharField(choices=[('DOWNVOTE', 'DOWNVOTE'), ('UPVOTE', 'UPVOTE')], max_length=50, null=True),
        ),
    ]
