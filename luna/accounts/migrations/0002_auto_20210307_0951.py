# Generated by Django 3.1.6 on 2021-03-07 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='acc_id',
            new_name='account_id',
        ),
    ]
