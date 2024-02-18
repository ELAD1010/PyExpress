from lib.app import App
from lib.router import Router


def main():
    app = App('localhost', 80)

    router = Router('/cat')

    @app.get('/name')
    def get_name(request, response):
        print(request)
        response.send('hello')

    @router.get('/name')
    def get_cat_name(request, response):
        pass

    app.add_router(router)

    app.run()


if __name__ == "__main__":
    main()
