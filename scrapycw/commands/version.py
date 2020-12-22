import os

from scrapycw.commands import ScrapycwCommand
from scrapycw.core.response import Response


class Command(ScrapycwCommand):

    can_print_result = True

    def run(self, args, opts):
        # TODO 代码抽离，Web端也要展示
        return Response(data={"version": open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "VERSION")).read()})

    def short_desc(self):
        return "version"

    def long_desc(self):
        return "version"
