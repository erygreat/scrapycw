import os
from scrapycw.utils.scrapycw import get_root_dir


def version():
    return {"version": open(os.path.join(get_root_dir(), "VERSION")).read()}
