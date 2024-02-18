from httper.common.app_router import AppRouter


class Router(AppRouter):
    def __init__(self, base_path: str):
        super().__init__()
        self.base_path = AppRouter._fix_path(base_path)
