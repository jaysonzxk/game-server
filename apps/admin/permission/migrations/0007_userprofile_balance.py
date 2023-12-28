# Generated by Django 2.2.16 on 2023-12-07 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0006_userprofile_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='余额'),
        ),
    ]
