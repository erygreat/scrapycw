from scrapycw.commands.spiders import Command


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def test_all_spiders():
    opts = Dict()
    opts['project'] = None
    r = Command().run([], opts)
    assert(r.success)
    assert(r.code == 0)
    assert(not r.message)
    for item in r.data:
        assert(item['project'] in ['default', 'demo', 'project2', 'new_project'])
        if item['project'] == 'default':
            item['spiders'] = ['baidu', 'baidu_log', 'ip_taobao']
        else:
            item['spiders'] = []


def test_spiders():
    opts = Dict()
    opts['project'] = 'default'
    r = Command().run([], opts)
    assert(r.success)
    assert(r.code == 0)
    assert(not r.message)
    assert(r.data['project'] == 'default')
    assert(r.data['spiders'] == ['baidu', 'baidu_log', 'ip_taobao'])
