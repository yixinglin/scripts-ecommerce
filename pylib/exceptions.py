
class InvalidEmailAddress(RuntimeError):
    def __init__(self, addr="*", *args, **kwargs):
        self.addr = addr
        pass
    def __str__(self):
        return f"InvalidEmailAddress <{self.addr}>"

class SendEmailNotPermitted(RuntimeError):
    def __init__(self, addr="*", *args, **kwargs):
        self.addr = addr
        pass
    def __str__(self):
        return f"SendEmailNotPermitted <{self.addr}>"

class CanceledSubscription(RuntimeError):

    def __init__(self, addr="*", *args, **kwargs):
        self.addr = addr
        pass
    def __str__(self):
        return f"SendEmailNotPermitted <{self.addr}>"

class InactivePeriodError(RuntimeError):
    def __init__(self, msg, *args, **kwargs):
        self.msg = msg
    def __str__(self):
        return f"InactivePeriodError {self.msg}"