class Response:
    def __init__(self, status_code):
        self.status_code = status_code
        self.data = ''

    def status(self, status_code):
        self.status_code = status_code
        return self

    def send(self, data):
        self.data = data
        return self
