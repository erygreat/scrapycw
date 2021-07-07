from scrapycw.services.job import Service
from scrapycw.commands import ScrapycwCommand


class Command(ScrapycwCommand):

    def run(self, args, opts):
        job_id = None
        if len(args) != 0:
            job_id = args[0]

        return Service.stats(
            job_id=job_id,
            is_parse_settings=opts.settings,
            is_parse_log=opts.log,
            is_parse_stats=opts.stats,
            is_parse_est=opts.est,
        )

    def short_desc(self):
        return "Job Stats"

    def long_desc(self):
        return "Job Stats"

    def syntax(self):
        return "<job-id> [options]"

    def add_options(self, parser):
        parser.add_option("--settings", help="是否输出 settings", action="store_true", default=False)
        parser.add_option("--log", help="是否输出日志信息", action="store_true", default=False)
        parser.add_option("--stats", help="是否输出任务 stats", action="store_true", default=False)
        parser.add_option("--est", help="是否输出运行中的 est (如果任务没有运行，则输出 None)", action="store_true", default=False)
