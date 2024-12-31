import os
from quickreplybottom import *
from databaseGS import Database
from getStringFromLine import *
from delete import deleteData
import param
from audit import *
from flask import Flask, request, abort
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    QuickReply,
    QuickReplyItem,
    PostbackAction,
    MessageAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    PostbackEvent
)
BOT_MODE = 0

app = Flask(__name__)

handler = WebhookHandler(os.environ['LINE_BOT_SECRET'])
configuration = Configuration(access_token=os.environ['LINE_BOT_ACCESS_TOKEN'])

db = Database("credentials.json")

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if param.MODE == 1:
            # In accounting mode
            msg = event.message.text
            datas = dataStringList(msg)

            """
            ### DEBUG START
            message_texts = event.message.text.splitlines()
            message_text = str("")
            if len(message_texts) == 4:
                message_text = message_text + "Datetimes: " + message_texts[0] + "\n"
                message_text = message_text + "Type: " + message_texts[1] + "\n"
                message_text = message_text + "Amount: " + message_texts[2] + "\n"
                message_text = message_text + "Note: " + message_texts[3]
            elif len(message_texts) == 2:
                message_text = message_text + "Type: " + message_texts[0] + "\n"
                message_text = message_text + "Amount: " + message_texts[1]
            else:
                message_text = "Error"
            ### DEBUG END
            """

            last_ID = int(db.sheet.row_values(db.getRowCount())[0])
            string = [str(last_ID + 1), datas['action'], datas['type'], datas['values'],
                              datas['description'], datas['date'], datas['time']]
            #string = ("pay", "breakfast", 30, "no", "2024", "12", "16", 
            #          "07:00")
            db.insertToTable(string)
            quickReply = GenerateYesNoQuickBottom()
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text="已紀錄"
                    ), TextMessage(
                        text="是否繼續記帳？",
                        quick_reply=quickReply
                    )
                    ]
                )
            )
        elif param.MODE == 2:
            msg = event.message.text
            datas = db.getAuditInfo(msg)
            print(datas)
            #for data in datas:
            #    print(data)
            quickReply = GenerateAuditYesNoQuickBottom()
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text=auditDataToLineString(datas)
                        ), TextMessage(
                        text="是否繼續查帳？",
                        quick_reply=quickReply
                    )
                    ]
                )
            )
        elif param.MODE == 3:
            msg = event.message.text
            string = db.deleteData(msg)

            quickReply = GenerateDeleteYesNoQuickBottom()
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text=string
                        ), TextMessage(
                        text="是否繼續刪除？",
                        quick_reply=quickReply
                    )]
                )
            )
        if event.message.text == "Quick reply":
            quickReply = GenerateQuickBottom()
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text="請選擇項目",
                        quick_reply=quickReply
                    )]
                )
            )
        else:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)]
                )
            )

@handler.add(PostbackEvent)
def handle_postback(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        postback_data = event.postback.data
        if postback_data == 'postback':
            param.MODE = 1
            quickReply = GenerateModeQuickBottom()
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text="<INPUT FORMAT>\n>Year/Date/Time\n>Type\n>Amount\n>Note",
                        quick_reply=quickReply
                    )]
                )
            )
        elif postback_data == "Continue accounting mode":
            param.MODE = 1
            quickReply = GenerateModeQuickBottom()
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text="<INPUT FORMAT>\n>Year/Date/Time\n>(必須)Type\n>(必須)Amount\n>Note",
                        quick_reply=quickReply
                    )]
                )
            )
        elif postback_data == "Quit accounting mode":
            param.MODE = 0
        elif postback_data == "Continue audit mode":
            param.MODE = 2
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text="<INPUT FORMAT>\n" + \
                        ">(From)Year/Date/Time\n" +\
                        ">(To)Year/Date/Time\n" +\
                        ">(必須)Type1\n" +\
                        ">(非必須)Type2\n.\n.\n.\n" +\
                        ">(非必須)TypeN\n" +\
                        "(Type可填\"全\", 或者指定特定種類)"
                    )]
                )
            )
        elif postback_data == "Quit audit mode":
            param.MODE = 0
        elif postback_data == "Audit":
            param.MODE = 2
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text="<INPUT FORMAT>\n" + \
                        ">(From)Year/Date/Time\n" +\
                        ">(To)Year/Date/Time\n" +\
                        ">(必須)Type1\n" +\
                        ">(非必須)Type2\n.\n.\n.\n" +\
                        ">(非必須)TypeN\n" +\
                        "(Type可填\"全\", 或者指定特定種類)"
                    )]
                )
            )
        elif postback_data == "Delete":
            param.MODE = 3
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text="<INPUT FORMAT>\n" + \
                        ">(必須)Id1\n" +\
                        ">(非必須)Id2\n.\n.\n.\n" +\
                        ">(非必須)IdN"
                    )]
                )
            )
        elif postback_data == "Continue delete mode":
            param.MODE = 3
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text="<INPUT FORMAT>\n" + \
                        ">(必須)Id1\n" +\
                        ">(非必須)Id2\n.\n.\n.\n" +\
                        ">(非必須)IdN"
                    )]
                )
            )
        elif postback_data == "Quit delete mode":
            param.MODE = 0
        elif postback_data == 'date':
            date = event.postback.params['date']
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=date)]
                )
            )
        elif postback_data == 'time':
            time = event.postback.params['time']
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=time)]
                )
            )
        elif postback_data == 'datetime':
            datetime = event.postback.params['datetime']
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=datetime)]
                )
            )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host='0.0.0.0', port=port)

