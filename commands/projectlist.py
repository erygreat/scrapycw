from scrapy.utils.conf import get_config

from scrapycw.commands import ScrapycwCommand
from scrapycw.scrapyhandlers.project import ProjectHandler


class Command(ScrapycwCommand):

    can_print = True

    def run(self, args, opts):
        return ProjectHandler.list()

    def short_desc(self):
        return "List of project"

    def long_desc(self):
        return "List of project"
