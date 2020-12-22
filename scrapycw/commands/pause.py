from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers.job import JobPauseHelper


class Command(ScrapycwCommand):

    def run(self, args, opts):
        job_id = None
        if len(args) != 0:
            job_id = args[0]
        return JobPauseHelper(job_id=job_id).get_response()

    def short_desc(self):
        return "Pause Spider"

    def long_desc(self):
        return "Pause Spider"

    def syntax(self):
        return "<job-id>"
