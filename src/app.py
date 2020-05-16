from . import create_app

app = create_app()


def run():
    global app
    app.run(port="8084")
