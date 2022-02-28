import os

from slack_bolt.adapter.socket_mode import SocketModeHandler

from bot_test.modules.root import create_app

app = create_app(token=os.environ.get("SLACK_BOT_TOKEN"))
SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
