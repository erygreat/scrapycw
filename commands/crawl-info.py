import sys

from scrapycw.commands import ScrapycwCommand
from scrapycw.django_manage import main
from scrapycw.utils.exception import ScrapycwUsageException
from scrapycw.web.api.models import SpiderJob


class Command(ScrapycwCommand):

    can_print_result = False

    def run(self, args, opts):
        task_id = opts.task_id
        model = SpiderJob.objects.filter(job_id=task_id).get()
        print(task_id)
        print(model.telnet_username)
        print(model.telnet_password)
        print(model.telnet_host)
        print(model.telnet_port)

    def short_desc(self):
        pass

    def long_desc(self):
        pass

    def add_options(self, parser):
        ScrapycwCommand.add_options(self, parser)
        parser.add_option("-t", "--task_id", dest="task_id", help="Task Id")

    def process_options(self, args, opts):
        ScrapycwCommand.process_options(self, args, opts)
        if opts.task_id is None:
            raise ScrapycwUsageException("Please enter task id")
