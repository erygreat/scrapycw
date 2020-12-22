from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers.job import JobListHelper


class Command(ScrapycwCommand):

    TYPE_CHOICES = ("all", "running", "finish", "pause", "closing")
    TYPE_DEFAULT = "all"

    def run(self, args, opts):
        return JobListHelper().get_response(
            offset=opts.offset,
            limit=opts.limit,
            spname=opts.spname,
            project=opts.project
        )

    def short_desc(self):
        return "Job List"

    def long_desc(self):
        return "Job List"

    def syntax(self):
        return "[options]"

    def add_options(self, parser):
        ScrapycwCommand.add_options(self, parser)
        parser.add_option("--offset", action="store", help="查询起始位置(分页)", type="int", default=0)
        parser.add_option("--limit", action="store", help="查询长度(分页)", type="int", default=10)
        parser.add_option("--spname", action="store", help="爬虫名称")
        parser.add_option("--type", action="store", help="类型 {}, 默认值为'{}'".format(self.TYPE_CHOICES, self.TYPE_DEFAULT), choices=self.TYPE_CHOICES)
        parser.add_option("--closed-reason", action="store", help="关闭原因, 默认值为'None', 参考值: finished, shutdown, cancelled")
