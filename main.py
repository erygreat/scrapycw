#!/Users/yaohongyin/spider/venv/bin/python3

# -*- coding: utf-8 -*-
import os
import re
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)) + "/..")

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    from scrapycw.cmdline import run
    sys.exit(run())
