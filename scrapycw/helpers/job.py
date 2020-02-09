from scrapycw.helpers import Helper
from scrapycw.utils.exception import ScrapycwException
from scrapycw.utils.telnet import ScrapycwTelnetException, Telnet
from scrapycw.web.api.models import SpiderJob


class ScrapycwJobException(ScrapycwException):
    pass


class JobHelper(Helper):

    def __init__(self, job_id=None):
        super().__init__()
        self.job_id = job_id

    def telnet_command(self, command):

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

        telnet = Telnet(host, port, username, password)
        telnet.connect()
        result = telnet.command(command)
        telnet.close()
        return result

    def stop(self):
        try:
            self.telnet_command("engine.stop()")
            return {"success": True, "message": "Finish", "status": "closing"}
        except ScrapycwJobException as e:
            return {"success": False, "message": "Error: {}".format(e.message)}
        except ScrapycwTelnetException as e:
            return {"success": False, "message": "Spider is Closed: {}".format(e.message), "status": "close"}

    def pause(self):
        try:
            self.telnet_command("engine.pause()")
            return {"success": True, "message": "Finish", "status": "pausing"}
        except ScrapycwJobException as e:
            return {"success": False, "message": "Error: {}".format(e.message)}
        except ScrapycwTelnetException as e:
            return {"success": False, "message": "Spider is Closed: {}".format(e.message), "status": "close"}

    def unpause(self):
        try:
            self.telnet_command("engine.unpause()")
            return {"success": True, "message": "Finish", "status": "running"}
        except ScrapycwJobException as e:
            return {"success": False, "message": "Error: {}".format(e.message)}
        except ScrapycwTelnetException as e:
            return {"success": False, "message": "Spider is Closed: {}".format(e.message), "status": "close"}

    # def est(self):
    #     try:
    #         result = self.telnet_command("est()")
    #         return {"success": True, "message": "Finish", "status": "running"}
    #     except ScrapycwJobException as e:
    #         return {"success": False, "message": "Error: {}".format(e.message)}
    #     except ScrapycwTelnetException as e:
    #         return {"success": False, "message": "Spider is Closed: {}".format(e.message), "status": "close"}