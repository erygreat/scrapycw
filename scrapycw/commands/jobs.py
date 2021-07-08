from scrapycw.utils.scrapycw import value_from_class
from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers.job import JobHelper
from scrapycw.services.job import Service


class Command(ScrapycwCommand):

    STATUS_CHOICES = (JobHelper.JOB_STATUS.RUNNING, JobHelper.JOB_STATUS.CLOSED)
    CLOSE_REASON_CHOICES = value_from_class(JobHelper.CLOSE_REASON)

    def run(self, args, opts):
        return Service.jobs(
            offset=opts.offset,
            limit=opts.limit,
            spider=opts.spider,
            project=opts.project,
            status=opts.status,
            close_reason=opts.close_reason
        )

    def short_desc(self):
        return "Job List"

    def long_desc(self):
        return "Job List"

    def syntax(self):
        return "[options]"

    def add_options(self, parser):
        parser.add_option("--offset", action="store", help="查询起始位置(分页, 默认为0)", type="int", default=0)
        parser.add_option("--limit", action="store", help="查询长度(分页, 默认为10)", type="int", default=10)
        parser.add_option("--project", action="store", help="项目名称")
        parser.add_option("--spider", action="store", help="爬虫名称")
        parser.add_option("--status", action="store", help="爬虫状态，默认查询所有，可选状态为: {}".format(self.STATUS_CHOICES))
        parser.add_option("--close-reason", action="store", help="关闭原因, 默认查询所有，常用状态为: {}，也可以添加自定义状态".format(self.CLOSE_REASON_CHOICES))
