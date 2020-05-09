from . import create_app


def run():
    app = create_app()
    app.run(port="8084")
