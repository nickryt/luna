# Generated by Django 3.2 on 2021-04-24 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_alter_account_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_picture',
            field=models.ImageField(default='/img/moolah.png', null=True, upload_to='img'),
        ),
    ]
