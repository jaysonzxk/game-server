# Generated by Django 2.2.16 on 2023-11-11 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20231109_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitor',
            name='isDel',
            field=models.IntegerField(default=0, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='sysfiles',
            name='isDel',
            field=models.IntegerField(default=0, null=True, verbose_name='是否删除'),
        ),
    ]
