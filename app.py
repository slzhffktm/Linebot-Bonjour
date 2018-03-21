# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#----------------------------------------------------
from commandBus import (
    resolve, getLink, getMovieData
)

from datetime import datetime


app = Flask(__name__)

line_bot_api = LineBotApi('KeiDaRmKlspzLPqz/PZ+rCU+oGwxglkbB1jH0vVXO3KpfNq90GLQ80QtzG38CuMGz+cqqR1vR+1noEUmL/5ebc23vxVNB5fcjYVEvJpuA5Go5Q5lNFG9uawxDw2byE929+BIqPb+q2xftN49xOGMCQdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('762ce4775c6e5ab75c9c2d65b99afb0a') #Your Channel Secret

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
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text #message from user

    if '#imdb' in text.split(' '):
        image_link = getLink(text.lower())
        movie_data = getMovieData(text.lower())
        line_bot_api.reply_message(
            event.reply_token,[
                ImageSendMessage(
                    original_content_url=image_link,
                    preview_image_url=image_link
                ),
                TextSendMessage(text=movie_data)
            ]
        )

    answer = resolve(text.lower())
    
    #get user profile
    if event.source.type == 'group':
        profile = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id) #get user profile
    elif event.source.type == 'room':
        profile = line_bot_api.get_room_member_profile(event.source.room_id, event.source.user_id)
    else:
        profile = line_bot_api.get_profile(event.source.user_id)

    d = datetime.now()

    if answer=='greeting':
        if d.hour<=11:
            reply = 'Good morning, ' + profile.display_name + '!'
        elif d.hour<=17 and d.hour>11:
            reply = 'Good afternoon, ' + profile.display_name + '!'
        elif d.hour<=21 and d.hour>17:
            reply = 'Good evening, ' + profile.display_name + '!'
        else:
            reply = 'Good night, ' + profile.display_name + '!'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)) #reply message
    elif answer=='leave':
        line_bot_api.reply_message(
            event.reply_token,[
                TextSendMessage(text='ih ' + profile.display_name + ' jahat sama aku :('), #reply message
                StickerSendMessage(
                package_id='1',
                sticker_id='9'
                )
            ]
        )
        line_bot_api.leave_room(event.source.room_id)
        line_bot_api.leave_group(event.source.group_id)
    elif answer=='jadwal':
        line_bot_api.reply_message(
            event.reply_token,[
                ImageSendMessage(
                    original_content_url='https://scontent-sit4-1.xx.fbcdn.net/v/t31.0-8/22550572_318376648570977_3387229290981069212_o.jpg?oh=0f55ae0a6fb24d6d5ffb1727619bcfd8&oe=5A80A4CC',
                    preview_image_url='https://scontent-sit4-1.xx.fbcdn.net/v/t31.0-8/22550572_318376648570977_3387229290981069212_o.jpg?oh=0f55ae0a6fb24d6d5ffb1727619bcfd8&oe=5A80A4CC'
                ),
                ImageSendMessage(
                    original_content_url='https://scontent-sit4-1.xx.fbcdn.net/v/t1.0-9/22491680_318376615237647_829250112634630959_n.jpg?oh=b3878ca608dc21963637f49935154215&oe=5A73F615',
                    preview_image_url='https://scontent-sit4-1.xx.fbcdn.net/v/t1.0-9/22491680_318376615237647_829250112634630959_n.jpg?oh=b3878ca608dc21963637f49935154215&oe=5A73F615'
                )
            ]
        )
    elif len(answer)>2000:
        line_bot_api.reply_message(
            event.reply_token,[
                TextSendMessage(text=answer[0:1999]),
                TextSendMessage(text=answer[2000:3999]) #reply message
            ]
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=answer)
        )
#--------------------------------------------------------------------------
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
