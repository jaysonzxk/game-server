# Generated by Django 2.2.16 on 2023-11-25 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0002_auto_20231121_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='paychannel',
            name='qrCode',
            field=models.CharField(blank=True, help_text='二维码', max_length=200, null=True, verbose_name='二维码'),
        ),
    ]
