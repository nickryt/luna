# Generated by Django 3.1.6 on 2021-03-07 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210307_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.FloatField(choices=[(-1, -1), (1, 1)], null=True)),
                ('post_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.post')),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.account')),
            ],
        ),
    ]
