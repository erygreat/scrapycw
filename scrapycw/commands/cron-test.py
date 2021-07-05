from apscheduler.schedulers.blocking import BlockingScheduler
from scrapycw.commands import ScrapycwCommand
from scrapycw.utils.slogger import get_logger
from scrapycw.web.app.models import SpiderJob



def myfunc():
    logger = get_logger("test")
    models = SpiderJob.objects.filter(
        status=SpiderJob.STATUS.RUNNING
    ).all()
    for model in models:
        logger.info(model.job_id)

class Command(ScrapycwCommand):

    def run(self, args, opts):
        scheduler = BlockingScheduler()
        print(scheduler.print_jobs())
        scheduler.add_job(myfunc, 'interval', seconds=10, id='my_job_id')
        scheduler.start()
        print(scheduler.get_jobs())


    def short_desc(self):
        return "Pause Spider"

    def long_desc(self):
        return "Pause Spider"

    def syntax(self):
        return "<job-id>"
