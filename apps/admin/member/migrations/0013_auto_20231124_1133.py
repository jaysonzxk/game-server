# Generated by Django 2.2.16 on 2023-11-24 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0012_auto_20231121_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vipcard',
            name='isDefault',
        ),
        migrations.AddField(
            model_name='vipcard',
            name='recommend',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='是否推荐'),
        ),
    ]
