class Quotex(BaseException):
    def __init__(self, message):
        self.message = message
#hi from d4rk3st

class QuotexAuthError(BaseException):
    def __init__(self, message):
        self.message = message


class QuotexParser(BaseException):
    def __init__(self, message):
        self.message = message


class QuotexTimeout(BaseException):
    def __init__(self, message):
        self.message = message
