from scrapycw.helpers import Helper
from scrapycw.utils.exception import ScrapycwException
from scrapycw.utils.telnet import Telnet, ScrapycwAuthenticationFailException, ScrapycwTelnetException
from scrapycw.web.api.models import SpiderJob


class ScrapycwJobException(ScrapycwException):
    pass


class JobHelper(Helper):

    def __init__(self, job_id=None):
        super().__init__()
        self.job_id = job_id

    def stop(self):

        if self.job_id is None:
            raise ScrapycwJobException("Please enter job id")
        try:
            model = SpiderJob.objects.get(job_id=self.job_id)
        except SpiderJob.DoesNotExist:
            raise ScrapycwJobException("Don't have job id: [{}]".format(self.job_id))

        host = model.telnet_host
        port = model.telnet_port
        username = model.telnet_username
        password = model.telnet_password

        try:
            telnet = Telnet(host, port, username, password)
            telnet.connect()
            telnet.command("engine.stop()")
            telnet.close()
            return {
                "success": True,
                "project": model.project,
                "spider": model.spider,
                "message": "Finish",
                "status": "pending"
            }
        except ScrapycwAuthenticationFailException as e:
            # 密码错误，大概率是这个爬虫已经被关闭了
            return {
                "success": False,
                "project": model.project,
                "spider": model.spider,
                "message": "Spider is Closed: Authentication failed",
                "status": "close"
            }
        except ScrapycwTelnetException as e:
            return {
                "success": False,
                "project": model.project,
                "spider": model.spider,
                "message": "Spider is Closed: {}".format(e.message),
                "status": "close"
            }

    def pause(self, job_id):
        pass
