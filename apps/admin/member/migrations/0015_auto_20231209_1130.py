# Generated by Django 2.2.16 on 2023-12-09 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0014_uservip_isexpiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservip',
            name='status',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='状态'),
        ),
    ]
