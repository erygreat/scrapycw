from scrapycw.commands import ScrapycwCommand
from scrapycw.services.spider import Service


class Command(ScrapycwCommand):

    def run(self, args, opts):
        return Service.list(project=opts.project)

    def short_desc(self):
        return "List of Spider"

    def long_desc(self):
        return "List of Spider"

    def syntax(self):
        return "[option]"

    def add_options(self, parser):
        parser.add_option("-p", "--project", action="store", help="项目名称，没有 project 则查询所有爬虫")
