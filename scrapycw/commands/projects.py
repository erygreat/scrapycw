from scrapycw.commands import ScrapycwCommand
from scrapycw.services.project import Service


class Command(ScrapycwCommand):

    def syntax(self):
        return ""

    def run(self, args, opts):
        return Service().list()

    def short_desc(self):
        return "List of project"

    def long_desc(self):
        return "List of project"
