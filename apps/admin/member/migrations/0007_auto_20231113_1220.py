# Generated by Django 2.2.16 on 2023-11-13 12:20

import apps.admin.op_drf.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('member', '0006_userexchangeconfig_isdel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userexchangeconfig',
            name='name',
        ),
        migrations.AddField(
            model_name='userexchangeconfig',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserExchangeConfig_user', to=settings.AUTH_USER_MODEL, verbose_name='关联用户'),
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', apps.admin.op_drf.fields.DescriptionField(blank=True, default='', help_text='描述', null=True, verbose_name='描述')),
                ('modifier', apps.admin.op_drf.fields.ModifierCharField(blank=True, help_text='该记录最后修改者', max_length=255, null=True, verbose_name='修改者')),
                ('isDel', models.IntegerField(default=0, null=True, verbose_name='是否删除')),
                ('dept_belong_id', models.CharField(blank=True, max_length=64, null=True, verbose_name='数据归属部门')),
                ('update_datetime', apps.admin.op_drf.fields.UpdateDateTimeField(auto_now=True, help_text='修改时间', null=True, verbose_name='修改时间')),
                ('create_datetime', apps.admin.op_drf.fields.CreateDateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=40, null=True, verbose_name='交易所名称')),
                ('status', models.IntegerField(default=0, null=True, verbose_name='状态')),
                ('creator', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '交易所配置',
                'verbose_name_plural': '交易所配置',
            },
        ),
        migrations.AddField(
            model_name='userexchangeconfig',
            name='exchange',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserExchangeConfig_exchange', to='member.Exchange', verbose_name='关联交易所'),
        ),
    ]
