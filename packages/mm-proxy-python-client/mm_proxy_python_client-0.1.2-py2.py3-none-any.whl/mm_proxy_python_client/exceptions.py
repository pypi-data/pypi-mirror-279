class HTTPError(Exception):
    message = "Network problem accessing MM-Proxy API. Exception: \n {}"

    def __init__(self, error_msg):
        self.message = self.message.format(error_msg)
        super(HTTPError, self).__init__(self.message)
