# Generated by Django 2.2.16 on 2023-11-14 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_payorders_purchaserobotorders_purchaseviporders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payorders',
            name='status',
            field=models.IntegerField(default=1, null=True, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='purchaserobotorders',
            name='status',
            field=models.IntegerField(default=1, null=True, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='purchaseviporders',
            name='status',
            field=models.IntegerField(default=1, null=True, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='quantifyorders',
            name='status',
            field=models.IntegerField(default=1, null=True, verbose_name='状态'),
        ),
    ]
