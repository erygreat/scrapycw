from scrapycw.core.REPONSE_CODE import RESPONSE_CODE


class Response(dict):
    message = None
    success = True
    data = None
    code = RESPONSE_CODE.SUCCESS

    def __init__(self, success=True, message=None, code=RESPONSE_CODE.SUCCESS, data=None):
        self.success = success
        self.message = message
        self.code = code
        self.data = data
        dict.__init__(self, {
            "success": self.success,
            "message": self.message,
            "code": self.code,
            "data": self.data
        })
