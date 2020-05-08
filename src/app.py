from . import create_app
def run():
    print("Hey")
    app = create_app()
    app.run(port="8084")

