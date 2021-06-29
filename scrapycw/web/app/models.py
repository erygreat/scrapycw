from django.db import models


class SpiderJob(models.Model):

    class STATUS(models.IntegerChoices):
        RUNNING = 1
        CLOSED = 2

    id = models.AutoField(primary_key=True)
    job_id = models.CharField(max_length=50, null=False, unique=True, verbose_name="任务ID")
    project = models.CharField(max_length=255, null=False, verbose_name="项目名称")
    spider = models.CharField(max_length=255, null=False, verbose_name="爬虫名称")
    spargs = models.TextField(default="", verbose_name="爬虫参数")
    cmdline_settings = models.TextField(default="{}", verbose_name="settings 信息")
    telnet_username = models.CharField(max_length=50, null=False, verbose_name="Telnet 用户名")
    telnet_password = models.CharField(max_length=50, null=False, verbose_name="Telnet 密码")
    telnet_host = models.CharField(max_length=50, null=False, verbose_name="Telnent 地址")
    telnet_port = models.IntegerField(null=False, verbose_name="Telnet 端口")
    status = models.IntegerField(choices=STATUS.choices, null=False, default=STATUS.RUNNING, verbose_name="当前状态: {}".format(STATUS.choices))
    log_file = models.CharField(max_length=255, null=True, verbose_name="日志路径")
    start_time = models.DateTimeField(null=True, default=None, verbose_name="任务开始时间")
    end_time = models.DateTimeField(null=True, default=None, verbose_name="任务结束时间")
    close_reason = models.CharField(max_length=50, null=True, default=None, verbose_name="关闭原因")
    stats = models.TextField(default="{}", verbose_name="stat 信息")
    settings = models.TextField(default="{}", verbose_name="settings 信息")
    log_info = models.TextField(default="{}", verbose_name="log 信息")
    page_count = models.IntegerField(verbose_name="page count")
    item_count = models.IntegerField(verbose_name="item count")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "spider_job"
        indexes = [
            models.Index(fields=['project', 'spider'], name='idx_project_spider'),
            models.Index(fields=['status'], name='idx_status'),
            models.Index(fields=['close_reason'], name='idx_close_reason'),
        ]
