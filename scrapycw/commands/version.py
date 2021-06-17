from scrapycw.commands import ScrapycwCommand
from scrapycw.services.version import Service


class Command(ScrapycwCommand):

    can_print_result = True

    def run(self, args, opts):
        return Service.version()

    def short_desc(self):
        return "version"

    def long_desc(self):
        return "version"
