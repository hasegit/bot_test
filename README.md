# bot_test
Boltを試しに使ってみたプロジェクトです。
Socket Modeでの利用を前提としています。

## 実行方法
1. pyenv/poetryで環境を整えます
```
pyenv local 3.10.2
poetry install
poetry shell
```
2. SLACK_APP_TOKENとSLACK_BOT_TOKENを環境変数に設定します
```
export SLACK_APP_TOKEN=xapp-xxxxxxxxxxxxx
export SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxx
```
3. 起動します
```
python -m bot_test
```
4. slackでBotに対して `@<bot> action` とメンションを飛ばします
5. attachmentが表示されるのでボタンをクリックします
6. modalが起動するので、適当に選択します
7. 選択結果がDMで連携されます

## 参考
### blockなどの作成
[Block Kit Builder](https://app.slack.com/block-kit-builder)で行い、できたらコピペする。
