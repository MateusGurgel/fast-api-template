class HttpException(Exception):
    def __init__(self, code, body):
        super().__init__(body)
        self.code = code
        self.body = body
