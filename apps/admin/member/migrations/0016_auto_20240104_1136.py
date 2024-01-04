# Generated by Django 2.2.16 on 2024-01-04 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20240104_1136'),
        ('member', '0015_auto_20231209_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='robot',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='userexchangeconfig',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='userexchangeconfig',
            name='exchange',
        ),
        migrations.RemoveField(
            model_name='userexchangeconfig',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userrobot',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='userrobot',
            name='robot',
        ),
        migrations.RemoveField(
            model_name='userrobot',
            name='user',
        ),
        migrations.DeleteModel(
            name='Exchange',
        ),
        migrations.DeleteModel(
            name='Robot',
        ),
        migrations.DeleteModel(
            name='UserExchangeConfig',
        ),
        migrations.DeleteModel(
            name='UserRobot',
        ),
    ]
