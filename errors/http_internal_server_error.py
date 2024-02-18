from http import HTTPStatus


class HttpInternalServerError(Exception):
    def __init__(self):
        super().__init__()
        self.message = "Internal server error"
        self.status = HTTPStatus.INTERNAL_SERVER_ERROR

