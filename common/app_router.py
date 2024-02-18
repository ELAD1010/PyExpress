class AppRouter:
    def __init__(self):
        self.routes = {'GET': {}, 'POST': {}, 'PUT': {}, 'PATCH': {}, 'DELETE': {}}
        self.base_path = ""

    def get(self, path, status_code=200):
        path = self.base_path + AppRouter._fix_path(path)

        def inner(func):
            self.routes['GET'][path] = {'handler': func, 'status': status_code}
        return inner  # this is the func_obj mentioned in the above content

    def post(self, path: str, status_code=201):
        path = self.base_path + AppRouter._fix_path(path)

        def inner(func):
            self.routes['POST'][path] = { 'handler': func, 'status': status_code }

        return inner

    @staticmethod
    def _fix_path(path):
        if not path.startswith("/"):
            path = f'/{path}'
        return path
