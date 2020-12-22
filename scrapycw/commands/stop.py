from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers.job import JobStopHelper


class Command(ScrapycwCommand):

    def run(self, args, opts):
        job_id = None
        if len(args) != 0:
            job_id = args[0]
        return JobStopHelper(job_id=job_id).get_response()

    def short_desc(self):
        return "Stop Spider"

    def long_desc(self):
        return "Stop Spider"

    def syntax(self):
        return "<job-id>"
