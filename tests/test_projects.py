from scrapycw.commands.projects import Command


def test_projects():
    r = Command().run([], {})
    assert(r.success)
    assert(r.code == 0)
    assert(not r.message)
    assert(r.data == ['default', 'demo', 'project2', 'new_project'])
