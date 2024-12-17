from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, StickerSendMessage, ImageSendMessage

from datetime import datetime

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

def index(request):
    return HttpResponse("Hello Line Bot works~!")

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:

            # 若有訊息事件
            if isinstance(event, MessageEvent):

                currentDateAndTime = datetime.now()
                currentTime = currentDateAndTime.strftime("%H:%M:%S")

                txtmsg = "您所傳的訊息是:\n"
                txtmsg = currentTime + "\n"
                txtmsg += event.message.text

                # 回傳收到的文字訊息
                line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text = txtmsg ),

                    StickerSendMessage(package_id=1070, sticker_id=17842),
                    
                    ImageSendMessage(original_content_url='https://d3gjxtgqyywct8.cloudfront.net/o2o/image/961f8641-dcbe-4205-b75c-0246a292b6c4.jpg'),

                    LocationSendMessage(title='文澡外語大學', address='Wenzao Ursuline University of Languages', latitude=22.670419222110695, longitude=120.31825742491581)
                    ])

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
