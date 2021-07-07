from scrapy.exceptions import UsageError
from scrapycw.commands import ScrapycwCommand
from scrapycw.services.job import Service


class Command(ScrapycwCommand):

    def run(self, args, opts):
        job_id = None
        if len(args) == 0:
            raise UsageError()
        job_id = args[0]
        return Service.stop(job_id=job_id)

    def short_desc(self):
        return "Stop Spider"

    def long_desc(self):
        return "Stop Spider"

    def syntax(self):
        return "<job-id>"

    def add_options(self, parser):
        pass