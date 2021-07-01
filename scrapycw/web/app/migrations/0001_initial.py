# Generated by Django 3.1.12 on 2021-07-01 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SpiderJob',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('job_id', models.CharField(max_length=50, unique=True, verbose_name='任务ID')),
                ('project', models.CharField(max_length=255, verbose_name='项目名称')),
                ('spider', models.CharField(max_length=255, verbose_name='爬虫名称')),
                ('spargs', models.TextField(default='{}', verbose_name='爬虫参数')),
                ('cmdline_settings', models.TextField(default='{}', verbose_name='settings 信息')),
                ('telnet_username', models.CharField(max_length=50, verbose_name='Telnet 用户名')),
                ('telnet_password', models.CharField(max_length=50, verbose_name='Telnet 密码')),
                ('telnet_host', models.CharField(max_length=50, verbose_name='Telnent 地址')),
                ('telnet_port', models.IntegerField(verbose_name='Telnet 端口')),
                ('status', models.IntegerField(choices=[(1, 'Running'), (2, 'Closed')], default=1, verbose_name="当前状态: [(1, 'Running'), (2, 'Closed')]")),
                ('log_file', models.CharField(max_length=255, null=True, verbose_name='日志路径')),
                ('start_time', models.DateTimeField(null=True, verbose_name='任务开始时间')),
                ('end_time', models.DateTimeField(null=True, verbose_name='任务结束时间')),
                ('close_reason', models.CharField(max_length=50, null=True, verbose_name='关闭原因')),
                ('stats', models.TextField(null=True, verbose_name='stat 信息')),
                ('settings', models.TextField(null=True, verbose_name='settings 信息')),
                ('log_info', models.TextField(null=True, verbose_name='log 信息')),
                ('page_count', models.IntegerField(null=True, verbose_name='page count')),
                ('item_count', models.IntegerField(null=True, verbose_name='item count')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'spider_job',
            },
        ),
        migrations.AddIndex(
            model_name='spiderjob',
            index=models.Index(fields=['project', 'spider'], name='idx_project_spider'),
        ),
        migrations.AddIndex(
            model_name='spiderjob',
            index=models.Index(fields=['status'], name='idx_status'),
        ),
        migrations.AddIndex(
            model_name='spiderjob',
            index=models.Index(fields=['close_reason'], name='idx_close_reason'),
        ),
    ]
