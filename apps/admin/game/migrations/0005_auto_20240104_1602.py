# Generated by Django 2.2.16 on 2024-01-04 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20240104_1540'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='games',
            options={'verbose_name': '厂商名称', 'verbose_name_plural': '厂商名称'},
        ),
        migrations.RenameField(
            model_name='gamecategory',
            old_name='icon',
            new_name='uri',
        ),
        migrations.RenameField(
            model_name='games',
            old_name='cover',
            new_name='uri',
        ),
    ]