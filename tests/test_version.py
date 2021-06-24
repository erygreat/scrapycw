from scrapycw.commands.version import Command
import re


def test_version():
    result = Command().run({}, [])
    assert(result.success)
    assert(result.message is None)
    assert(result.code == 0)
    assert(re.search(r"^\d+\.\d+\.\d+$", result.data['version']) is not None)
