from scrapycw.services.job import Service
from scrapycw.commands import ScrapycwCommand

class Command(ScrapycwCommand):

    def run(self, args, opts):
        job_id = None
        if len(args) != 0:
            job_id = args[0]
        return Service.pause(job_id=job_id)

    def short_desc(self):
        return "Pause Spider"

    def long_desc(self):
        return "Pause Spider"

    def syntax(self):
        return "<job-id>"

    def add_options(self, parser):
        pass