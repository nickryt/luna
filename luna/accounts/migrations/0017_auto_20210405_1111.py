# Generated by Django 3.1.6 on 2021-04-05 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20210405_1055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='post_id',
            new_name='post',
        ),
    ]