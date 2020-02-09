from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers.job import JobHelper


class Command(ScrapycwCommand):

    def run(self, args, opts):
        job_id = None
        if len(args) != 0:
            job_id = args[0]

        return JobHelper(job_id=job_id).status(opts.parse_settings, opts.parse_stats, opts.parse_log)

    def short_desc(self):
        return "Run Spider"

    def long_desc(self):
        return "Run Spider"

    def syntax(self):
        return "<job-id>"

    def add_options(self, parser):
        ScrapycwCommand.add_options(self, parser)
        parser.add_option("--parse-settings", help="是否解析settings", action="store_true", default=False)
        parser.add_option("--parse-log", help="是否解析log", action="store_true", default=False)
        parser.add_option("--parse-stats", help="是否解析stats", action="store_true", default=False)

