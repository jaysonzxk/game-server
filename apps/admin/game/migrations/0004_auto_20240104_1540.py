# Generated by Django 2.2.16 on 2024-01-04 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20231228_1834'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='games',
            options={'verbose_name': '三方游戏', 'verbose_name_plural': '三方游戏'},
        ),
        migrations.RenameField(
            model_name='gamecategory',
            old_name='uri',
            new_name='icon',
        ),
        migrations.RenameField(
            model_name='games',
            old_name='uri',
            new_name='cover',
        ),
        migrations.AlterField(
            model_name='games',
            name='gameManufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gameManufacturer', to='game.GameCategory', verbose_name='关联大类'),
        ),
        migrations.DeleteModel(
            name='GameManufacturer',
        ),
    ]
