import os

from scrapy.exceptions import UsageError
from scrapy.extension import ExtensionManager
from scrapy.utils.conf import arglist_to_dict
from scrapy.utils.python import without_none_values

from scrapycw.commands import ScrapycwCommand


class Command(ScrapycwCommand):

    can_crawl_log_print = True

    def long_desc(self):
        return "Run a spider"

    def syntax(self):
        return "[options] <spider>"

    def short_desc(self):
        return "Run a spider"

    def add_options(self, parser):
        ScrapycwCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE", help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE", help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT", help="format to use for dumping items with -o")

    def process_options(self, args, opts):
        ScrapycwCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
        if opts.output:
            if opts.output == '-':
                self.settings.set('FEED_URI', 'stdout:', priority='cmdline')
            else:
                self.settings.set('FEED_URI', opts.output, priority='cmdline')
            feed_exporters = without_none_values(self.settings.getwithbase('FEED_EXPORTERS'))
            valid_output_formats = feed_exporters.keys()
            if not opts.output_format:
                opts.output_format = os.path.splitext(opts.output)[1].replace(".", "")
            if opts.output_format not in valid_output_formats:
                raise UsageError("Unrecognized output format '%s', set one"
                                 " using the '-t' switch or as a file extension"
                                 " from the supported list %s" % (opts.output_format,
                                                                  tuple(valid_output_formats)))
            self.settings.set('FEED_FORMAT', opts.output_format, priority='cmdline')

    def run(self, args, opts):
        if len(args) < 1:
            raise UsageError()
        elif len(args) > 1:
            raise UsageError("running 'scrapycw crawl' with more than one spider is no longer supported")
        spname = args[0]

        self.crawler_process.crawl(spname, **opts.spargs)
        # crawlers = list(self.crawler_process.crawlers)
        # for crawler in crawlers:
        #     print(crawler.engine.start_time)
        #     print(dir(crawler.engine))
        # self.crawler_process.start()

        crawlers = list(self.crawler_process.crawlers)
        for crawler in crawlers:
            print(crawler.extensions)
            print(dir(crawler.extensions))
            ExtensionManager

        if self.crawler_process.bootstrap_failed:
            self.exitcode = 1
