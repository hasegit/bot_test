from slack_bolt import App

from .check_server import check_server


def create_app(token: str) -> App:
    # create app
    app = App(token=token)

    # setup functions
    check_server.CheckServer(app)

    return app
