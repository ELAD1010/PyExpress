from lib.sniffer import HttpSniffer

from httper.common.app_router import AppRouter
from httper.lib.response_sender import ResponseSender
from httper.lib.router import Router


class App(AppRouter):
    def __init__(self, ip, port):
        super().__init__()
        self.responder = ResponseSender(self.routes)
        self.sniffer = HttpSniffer(ip, port, self.responder)

    def run(self):
        self.sniffer.start()
        self.responder.start()

        self.sniffer.join()
        self.responder.join()

    def add_router(self, router: Router):
        for method in router.routes.keys():
            for path in router.routes[method].keys():
                self.routes[method][path] = router.routes[method][path]
