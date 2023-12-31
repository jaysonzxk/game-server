# Generated by Django 2.2.16 on 2023-11-11 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0002_auto_20231110_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='dept',
            name='isDel',
            field=models.IntegerField(default=0, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='menu',
            name='isDel',
            field=models.IntegerField(default=0, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='post',
            name='isDel',
            field=models.IntegerField(default=0, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='role',
            name='isDel',
            field=models.IntegerField(default=0, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='isDel',
            field=models.IntegerField(default=0, null=True, verbose_name='是否删除'),
        ),
    ]
