import json
from copy import deepcopy


class CheckServer:
    def __init__(self, app):
        """
        initでappに対して関数を追加していく
        各種blockはjsonとして外出しし、initで読み込む
        (各関数で読み込むと毎回I/Oが走るので、それを防ぐ)
        """

        # blockのload
        # attachment
        with open("bot_test/modules/check_server/attachment.json", encoding="utf-8") as f:
            self.attachment = json.loads(f.read())

        # modal
        with open("bot_test/modules/check_server/check_server_modal.json", encoding="utf-8") as f:
            self.check_view = json.loads(f.read())

        # appのSetup。処理の流れとしては、
        # - メンションつきのメッセージでBotがAttachmentを表示
        # - 表示されたAttachmentから実行したい処理のボタンをクリック
        # - modalが表示されるので、必要事項を選択し、submit
        # - modalのsubmitをリスニングし、送信時にアクションを実行
        app.event("app_mention")(self.mention)
        app.action("check_server")(self.action_check_server)
        app.view("check_server")(self.handle_check_server_submission)

        # app_mentionを拾うとmessageのeventを拾っていないと文句を言われるので以下で回避
        # 正しい処理なのかは不明
        app.event("message")(lambda: None)

    def mention(self, event, say):
        # mentionのテキストを抽出
        # @bot hogeのhoge以降の部分
        # messageにおいて、@botとhogeの間にスペースを入れないことも可能だが
        # そのケースはいったん対応しない
        cmd = " ".join(event["text"].split(" ")[1:])

        # mentionのテキストによって処理を変える
        # 今回はactionという単語に反応
        match cmd:
            case "action":
                # actionの場合は、actionを選択するボタンを並べたattachmentを表示
                say(attachments=self.attachment["attachments"])
            case _:
                say("ちょっと何言ってるか分からないです")

    def action_check_server(self, ack, body, client):
        # attachmentのボタンクリックで発火
        ack()

        # ボタンがクリックされたchannel IDの取得
        channel = body["channel"]["id"]

        # check_viewにchannel IDを埋め込む
        # インスタンス変数をいじるのはアレなので、deepcopyしてから
        check_view = deepcopy(self.check_view)
        check_view["private_metadata"] = channel
        client.views_open(trigger_id=body["trigger_id"], view=check_view)

    def handle_check_server_submission(self, ack, client, body, view):
        # modalのsubmitで発火
        servers = [
            s["value"]
            for s in view["state"]["values"]["server"]["target_server"]["selected_options"]
        ]
        command = view["state"]["values"]["command"]["command"]["selected_option"][
            "value"
        ].replace("_", " ")

        ack()

        # 選択結果をchannelに投稿
        msg = f"実行対象サーバ: {','.join(servers)}\n実行コマンド: {command}"
        channel = view["private_metadata"]
        client.chat_postMessage(channel=channel, text=msg)
