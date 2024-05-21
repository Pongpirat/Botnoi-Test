from flask import Flask, request, abort
from linebot import (
    LineBotApi,
    WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    QuickReply,
    QuickReplyButton,
    MessageAction,
    CarouselTemplate,
    CarouselColumn,
    URIAction
)

app = Flask(__name__)

# Channel Access Token และ Channel Secret ของ Line Bot
line_bot_api = LineBotApi('YM59T0COmHD+XNDZlJXMwQtaTrC+8fgFbP/348EJjqx7rPS60LiWTAkeSiQBiIym96VIQ4L41T1BRnFnHTi6zoKAAd2U0MY/pxjvI+MEldzSrV51539WH35IzrtSEZz92uSXnSrss1AvhWQA/r9yRwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('85ab0b57a8a27c8bbb7c34b56a64ea02')

# เชื่อมต่อ Line Bot ด้วยเส้นทาง /callback
@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# เมื่อมีการส่งข้อความมาจากผู้ใช้
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.lower()
    if text == 'text':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='This is a text message'))
    elif text == 'hello':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hello, user')
        )
    elif text == 'button':
        buttons_template = ButtonsTemplate(
            title='My buttons sample',
            text='Hello, please select:',
            actions=[
                MessageAction(label='Message', text='Hello'),
                MessageAction(label='Text', text='Text')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=buttons_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'quickreply':
        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="Yes", text="Yes")),
            QuickReplyButton(action=MessageAction(label="No", text="No"))
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Do you like Python?', quick_reply=quick_reply)
        )
        # เพิ่มฟังก์ชัน handle_message เพื่อตรวจสอบการกด Yes หรือ No และแสดงภาพตามที่ผู้ใช้เลือก
    elif text == 'yes':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Great! Python is awesome.')
        )
    elif text == 'no':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Oh no! What language do you prefer?')
        )
    elif text == 'carousel':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
                thumbnail_image_url='https://www.svgrepo.com/show/376344/python.svg',
                title='Python',
                text='Description 1',
                actions=[
                    URIAction(label='Go to Website', uri='https://www.python.org/'),
                    MessageAction(label='Say Hello', text='Hello')
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://res.cloudinary.com/practicaldev/image/fetch/s--IqXbCVrh--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://duckduckgo.com/i/77cac527.png',
                title='Golang',
                text='Description 2',
                actions=[
                    URIAction(label='Go to Website', uri='https://go.dev/'),
                    MessageAction(label='Say Hello', text='Hello')
                ]
            )
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=carousel_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Unknown command, please try again.'))

if __name__ == "__main__":
    app.run()
