from apscheduler.schedulers.blocking import BlockingScheduler
from scrapycw.commands import ScrapycwCommand
from scrapycw.core.slogger import getLogger
from scrapycw.helpers.job import JobStatusHelper
from scrapycw.web.api.models import SpiderJob

import time


class Command(ScrapycwCommand):

    def run(self, args, opts):
        models = SpiderJob.objects.filter(
            status=SpiderJob.STATUS.RUNNING
        ).all()
        for model in models:
            data = JobStatusHelper(job_id=model.job_id).get()
            print(data)

    def short_desc(self):
        return "Pause Spider"

    def long_desc(self):
        return "Pause Spider"

    def syntax(self):
        return "<job-id>"
