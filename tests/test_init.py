from scrapycw.commands.init import Command
import re


def test_init():
    Command().run({}, [])
