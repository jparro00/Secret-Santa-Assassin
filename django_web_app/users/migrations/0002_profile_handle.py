# Generated by Django 3.2.dev20201110203713 on 2020-11-23 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='handle',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
    ]