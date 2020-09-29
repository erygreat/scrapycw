from django.db import models


class SpiderJob(models.Model):

    class STATUS(models.IntegerChoices):
        RUNNING = 1
        FINISH = 2
        SHUTDOWN = 3
        FAIL = 4

    id = models.AutoField(primary_key=True)
    job_id = models.CharField(max_length=50, null=False, unique=True, verbose_name="job id")
    project = models.CharField(max_length=255, null=False, verbose_name="project")
    spider = models.CharField(max_length=255, null=False, verbose_name="spider")
    telnet_username = models.CharField(max_length=50, null=False, verbose_name="scrapy telnet username")
    telnet_password = models.CharField(max_length=50, null=False, verbose_name="scrapy telnet password")
    telnet_host = models.CharField(max_length=50, null=False, verbose_name="scrapy telnet host")
    telnet_port = models.IntegerField(null=False, verbose_name="scrapy telnet port")
    status = models.IntegerField(choices=STATUS.choices, null=False, default=STATUS.RUNNING, verbose_name="status: {}".format(STATUS.choices))
    log_file = models.CharField(max_length=255, null=True, verbose_name="log file path")
    job_start_time = models.DateTimeField(null=True, default=None, verbose_name="job start time")
    job_end_time = models.DateTimeField(null=True, default=None, verbose_name="job end time")
    stats = models.TextField(default="{}", verbose_name="stat info")
    settings = models.TextField(default="{}", verbose_name="settings info")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "spider_job"
        index_together = ["project", "spider"]

