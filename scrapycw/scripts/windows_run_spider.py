import optparse
import os
import sys
import json

from scrapy.utils.conf import closest_scrapy_cfg

def get_spider_windows_run_script_path():
    return os.path.abspath(__file__)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    project_dir = os.path.dirname(closest_scrapy_cfg())
    sys.path.insert(0, current_dir)
    sys.path.append(project_dir)

    # windows系统启动爬虫实现
    from scrapycw.helpers.spider import WindowsSpiderRunner
    from scrapycw.utils.scrapy_util import get_scrapy_settings
    argv = sys.argv
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter())
    group = optparse.OptionGroup(parser, "Global Options")
    group.add_option("--spname", action="store")
    group.add_option("--settings", action="store")
    group.add_option("--job_id", action="store")
    group.add_option("--spargs", action="store")
    group.add_option("--project", action="store")
    parser.add_option_group(group)
    opts, args = parser.parse_args(args=argv[1:])
    cmdline_settings = json.loads(opts.settings) if opts.settings else None 
    spargs = json.loads(opts.spargs) if opts.spargs else None
    project = opts.project
    settings = get_scrapy_settings(project)
    settings.setdict(cmdline_settings, priority='cmdline')
    WindowsSpiderRunner(
        spname=opts.spname,
        spargs=spargs,
        project=project,
        settings=settings,
        cmdline_settings=cmdline_settings,
        job_id=opts.job_id
    ).start_spider()
