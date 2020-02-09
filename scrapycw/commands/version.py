import os

from scrapycw.commands import ScrapycwCommand


class Command(ScrapycwCommand):

    can_print_result = True

    def run(self, args, opts):
        return {"version": open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "VERSION")).read()}

    def short_desc(self):
        return "version"

    def long_desc(self):
        return "version"
