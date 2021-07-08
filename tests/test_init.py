from scrapycw.commands.init import Command


def test_init():
    Command().run({}, [])
