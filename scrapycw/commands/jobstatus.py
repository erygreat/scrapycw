from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers.job import JobStatusHelper


class Command(ScrapycwCommand):

    def run(self, args, opts):
        job_id = None
        if len(args) != 0:
            job_id = args[0]

        return JobStatusHelper(job_id=job_id).get_response(is_parse_settings=opts.parse_settings, is_parse_stats=opts.parse_stats, is_parse_log=opts.parse_log)

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
