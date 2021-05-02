# Generated by Django 3.1.6 on 2021-03-07 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='vote',
            field=models.CharField(choices=[('DOWNVOTE', 'DOWNVOTE'), ('UPVOTE', 'UPVOTE')], max_length=20, null=True),
        ),
    ]