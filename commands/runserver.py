import multiprocessing
import os
import sys

from scrapy.utils.conf import get_config

from scrapycw.commands import ScrapycwCommand
from scrapycw.django_manage import main


class Command(ScrapycwCommand):

    can_print = True

    def run(self, args, opts):
        sys.argv = []
        sys.argv.append(os.path.abspath(os.path.dirname(__file__)) + "/../django_manage.py")
        sys.argv.append("runserver")
        sys.argv.append("{}:{}".format(opts.host, opts.port))
        #
        # pid = os.fork()
        # if pid:
        #     sys.exit(0)
        #
        # os.umask(0)
        # os.setsid()
        #
        # _pid = os.fork()
        # if _pid:
        #     sys.exit(0)
        #
        # sys.stdout.flush()
        # sys.stderr.flush()
        #
        # with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
        #     os.dup2(read_null.fileno(), sys.stdin.fileno())
        #     os.dup2(write_null.fileno(), sys.stdout.fileno())
        #     os.dup2(write_null.fileno(), sys.stderr.fileno())

        main()

    def short_desc(self):
        return "Run Web Service"

    def long_desc(self):
        return "Run Web Service"

    def add_options(self, parser):
        ScrapycwCommand.add_options(self, parser)
        parser.add_option("--port", metavar="<PORT>", help="web服务端口", default=8923, type="int")
        parser.add_option("--host", metavar="<HOST>", help="监听的IP地址，当为0时表示完全公开", default="localhost")
