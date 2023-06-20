from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, AudioSendMessage, VideoSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, URITemplateAction, PostbackTemplateAction, PostbackEvent, ConfirmTemplate, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, ImagemapSendMessage, BaseSize, MessageImagemapAction, ImagemapArea, URIImagemapAction, DatetimePickerTemplateAction, BubbleContainer, ImageComponent, BoxComponent, TextComponent, IconComponent, ButtonComponent, SeparatorComponent, FlexSendMessage, URIAction                   
from urllib.parse import parse_qsl
import datetime

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

# Create your views here.

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError():
            return HttpResponseBadRequest()
        
        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '@指令列表':
                        sendText(event)
                        
                    elif mtext == '@品牌圖片':
                        sendImage(event)
                        
                    elif mtext == '@哈囉':
                        sendStick(event)
                        
                    elif mtext == '@多項傳送':
                        sendMulti(event)
                        
                    elif mtext == '@傳送位置':
                        sendPosition(event)
                        
                    elif mtext == '@認識星巴克':
                       sendQuickreply(event)
                       
                    elif mtext == '@傳送聲音':
                        sendVoice(event)
                        
                    elif mtext == '@宣傳影片':
                        sendVideo(event)
                    
                    elif mtext == '@店面資訊':
                        sendButton(event)
                    
                    elif mtext == '@購買披薩':
                        sendPizza(event)
                        
                    elif mtext == '@確認購買':
                        sendConfirm(event)
                    
                    elif mtext == '@yes':
                        sendYes(event)
                        
                    elif mtext == '@no':
                        sendNo(event)
                    
                    elif mtext == '@飲品':
                        sendCarousel(event)
                    
                    elif mtext == '@午茶那堤組合':
                        sendImgCarousel(event)
                    
                    elif mtext == '@新品推薦':
                        sendImgmap(event)
                    
                    elif mtext == '@日期時間':
                        sendDatetime(event)
                    
                    elif mtext == '@生活用品':
                        sendFlex(event)
                        
                    elif mtext == '@特殊門市':
                        sendFlex1(event)
                    
                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mtext))
                        
            if isinstance(event, PostbackEvent):
                backdata = dict(parse_qsl(event.postback.data))
                if backdata.get('action') == 'buy':
                    sendBack_buy(event, backdata)
                if backdata.get('action') == 'sell':
                    sendData_sell(event, backdata)
                
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
    
    
    
def sendText(event):
    try:
        message = TextSendMessage(
                text = "請輸入以下的指令來獲得相關資訊 : \n@品牌圖片\n@哈囉 \n@傳送位置 \n@認識星巴克 \n@宣傳影片 \n@店面資訊 \n@飲品 \n@午茶那堤組合 \n@生活用品 \n@新品推薦 \n@特殊門市"
                
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='傳送文字發生錯誤!'))


def sendImage(event):
    try:
        message = ImageSendMessage(
                original_content_url = "https://i.imgur.com/JZdto0Z.png",
                preview_image_url = "https://i.imgur.com/JZdto0Z.png"
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='傳送圖片發生錯誤!'))
        
        
def sendStick(event):
    try:
        message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002738'
            
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
        
def sendMulti(event):
    try:
        message = [
            StickerSendMessage(
                    package_id='1',
                    sticker_id='2'
                ),
            TextSendMessage(
                    text = "這是 Pizza 圖片 !"
                ),
            ImageSendMessage(
                    original_content_url = "https://i.imgur.com/4QfKuz1.png",
                    preview_image_url = "https://i.imgur.com/4QfKuz1.png"
                )
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
        
        
def sendPosition(event):
    try:
        message = LocationSendMessage(
            title='星巴克 ( 中原大學門市 )',
            address='320桃園市中壢區中北路200號',
            latitude=24.957223743207297,
            longitude=121.24084311333094
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
        
        
def sendQuickreply(event):
    try:
        message = TextSendMessage(
            text='請選擇一個社群平台來認識我們吧!!',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                            action=MessageAction(label="facebook", text="https://www.facebook.com/starbuckstaiwan?ref=nf")
                        ),
                    QuickReplyButton(
                            action=MessageAction(label="instagram", text="https://www.instagram.com/starbuckstw/")
                        ),
                    QuickReplyButton(
                            action=MessageAction(label="youtube", text="https://www.youtube.com/user/STARBUCKSTW")
                        ),
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))        
        
        
        
        
def sendVoice(event):
    try:
        message = AudioSendMessage(
                original_content_url='https://14ee-2402-7500-568-721a-653a-15f2-8f7a-7590.ngrok.io/static/mario.m4a',
                duration=20000
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
        
        

def sendVideo(event):
    try:
        message = VideoSendMessage(
                original_content_url='https://0b77-2402-7500-477-be0a-eca9-4f3a-f5dd-b319.ngrok.io/static/starbucks.mp4',
                preview_image_url='https://0b77-2402-7500-477-be0a-eca9-4f3a-f5dd-b319.ngrok.io/static/starbucks3.png'
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
        
        
        
        
def sendButton(event):
    try:
        message = TemplateSendMessage(
            alt_text='店面資訊',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/JZdto0Z.png',
                title='星巴克店面資訊',
                text='請選擇 :',
                actions=[
                    MessageTemplateAction(
                        label='近期全店活動',
                        text='活動期間: 2022/6/20~6/21\n活動期間 16:00-20:00 購買兩杯相同容量/風味/冰熱一致的飲料，其中一杯由星巴克招待。'
                        ),
                    URITemplateAction(
                        label='星巴克線上門市',
                        uri='https://www.starbucks.com.tw/onlineshopping/index.jspx'
                        ),
                    URITemplateAction(
                        label='星巴克行動 APP',
                        uri='https://play.google.com/store/apps/details?id=com.starbucks.tw&utm_source=global_co&utm_medium=prtnr&utm_content=Mar2515&utm_campaign=PartBadge&pcampaignid=MKT-AC-global-none-all-co-pr-py-PartBadges-Oct1515-1'
                        ),
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))


def sendPizza(event):
    try:
        message = TextSendMessage(
                text = '感謝您購買披薩，我們將盡快為您製作。'
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))


def sendBack_buy(event, backdata):
    try:
        text1 = '請輸入@確認購買，\n如果您選擇是，'
        text1 += '\n我們將盡快為您製作。'
        message = TextSendMessage(
                text = text1
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
        


def sendConfirm(event):
    try:
        message = TemplateSendMessage(
            alt_text='確認樣板',
            template=ConfirmTemplate(
                text='你確定要購買這項商品嗎?',
                actions=[
                    MessageTemplateAction(
                        label='是',
                        text='@yes'
                        ),
                    MessageTemplateAction(
                        label='否',
                        text='@no'
                        )
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))


def sendYes(event):
    try:
        message = TextSendMessage(
                text='感謝您的購買，\n我們將盡快寄出商品。',
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))


def sendNo(event):
    try:
        message = TextSendMessage(
                text='沒關係，\n請您重新操作。',
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))



def sendCarousel(event):
    try:
        message = TemplateSendMessage(
            alt_text='飲品',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/kDEpAuN.jpg',
                        title='咖啡飲品',
                        text='濃郁豐厚的濃縮咖啡是我們咖啡的靈魂，調製成香氣迷人的咖啡',
                        actions=[
                            URITemplateAction(
                                    label='可可綿雲瑪奇朵',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=375&catId=2'
                                ),
                            URITemplateAction(
                                    label='那堤',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=1&catId=2'
                                ),
                            URITemplateAction(
                                    label='冰摩卡',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=10&catId=2'
                                )
                            ]
                        ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/1QLUDAO.jpg',
                        title='茶瓦納',
                        text='獨特創新的手作茶品體驗，獨具風味特性，帶著令人驚喜的風味元素',
                        actions=[
                            URITemplateAction(
                                    label='福吉茶那堤',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=299&catId=33'
                                ),
                            URITemplateAction(
                                    label='醇濃抹茶那堤',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=255&catId=33'
                                ),
                            URITemplateAction(
                                    label='冰玫瑰蜜香茶那堤',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=35&catId=33'
                                )
                            ]
                        ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/iHaioTh.jpg',
                        title='星冰樂',
                        text='沁涼無比的創新風味，清爽多層次口感星享受',
                        actions=[
                            URITemplateAction(
                                    label='榛果巧克力起司風味咖啡星冰樂',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=387&catId=5'
                                ),
                            URITemplateAction(
                                    label='焦糖可可碎片星冰樂',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=22&catId=5'
                                ),
                            URITemplateAction(
                                    label='綜合莓起司風味星冰樂',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=386&catId=6'
                                )
                            ]
                        ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/bop9itk.jpg',
                        title='冷萃咖啡',
                        text='獨特滑順沁涼典藏之作',
                        actions=[
                            URITemplateAction(
                                    label='夏日冰柚冷萃咖啡',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=388&catId=55'
                                ),
                            URITemplateAction(
                                    label='經典特調冷萃咖啡',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=241&catId=55'
                                ),
                            URITemplateAction(
                                    label='鹹焦糖風味綿雲氮氣冷萃咖啡',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=304&catId=55'
                                )
                            ]
                        ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/w3ttofh.jpg',
                        title='其他飲料',
                        text='甜美濃郁，無法抵擋的迷人滋味',
                        actions=[
                            URITemplateAction(
                                    label='經典巧克力',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=43&catId=11'
                                ),
                            URITemplateAction(
                                    label='冰經典巧克力',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=44&catId=11'
                                ),
                            URITemplateAction(
                                    label='兒童熱可可',
                                    uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=45&catId=11'
                                )
                            ]
                        )
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))



def sendImgCarousel(event):
    try:
        message = TemplateSendMessage(
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/EBmcJ5Y.jpg',
                        action=MessageTemplateAction(
                                label='巧克力焙茶起司蛋糕',
                                text='$240 / 組 ( + 中杯那堤 )'
                            )
                        ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/rcJzvta.jpg',
                        action=MessageTemplateAction(
                                label='栗子布蕾焦糖蛋糕',
                                text='$230 / 組 ( + 中杯那堤 )'
                            )
                        ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/sUC0rYG.jpg',
                        action=MessageTemplateAction(
                                label='雙星蕨餅套餐',
                                text='$220 / 組 ( + 中杯那堤 )'
                            )
                        ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/NzQaDiH.jpg',
                        action=MessageTemplateAction(
                                label='芋見雞肉鬆戚風三明治',
                                text='$240 / 組 ( + 中杯那堤 )'
                            )
                        ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/TFI8kJA.jpg',
                        action=MessageTemplateAction(
                                label='巴斯克風焦糖起司蛋糕',
                                text='$240 / 組 ( + 中杯那堤 )'
                            )
                        ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/lPkcOFx.jpg',
                        action=MessageTemplateAction(
                                label='經典輕乳蛋糕',
                                text='$190 / 組 ( + 中杯那堤 )'
                            )
                        )
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
        


def sendImgmap(event):
    try:
        image_url = 'https://i.imgur.com/n1nHVfJ.png'
        imgwidth = 1100
        imgheight = 600
        message = ImagemapSendMessage(
            base_url=image_url,
            alt_text='新品推薦',
            base_size=BaseSize(height=imgheight, width=imgwidth),
            actions=[
                URIImagemapAction(
                    link_uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=386&catId=6',
                    area=ImagemapArea(
                        x=0,
                        y=0,
                        width=imgwidth*0.5,
                        height=imgheight
                        )
                    ),
                URIImagemapAction(
                    link_uri='https://www.starbucks.com.tw/products/drinks/product.jspx?id=387&catId=6',
                    area=ImagemapArea(
                        x=imgwidth*0.5,
                        y=0,
                        width=imgwidth*0.5,
                        height=imgheight
                        )
                    ),
                ]
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))




def sendDatetime(event):
    try:
        message = TemplateSendMessage(
            alt_text='日期時間範例',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/VxVB46z.jpg',
                title='日期時間',
                text='請選擇 : ',
                actions=[
                    DatetimePickerTemplateAction(
                        label="選取日期",
                        data="action=sell&mode=date",
                        mode="date",
                        initial="2021-06-01",
                        min="2021-01-01",
                        max="2021-12-31"
                        ),
                    DatetimePickerTemplateAction(
                        label="選取時間",
                        data="action=sell&mode=time",
                        mode="time",
                        initial="10:00",
                        min="00:00",
                        max="23:59"
                        ),
                    DatetimePickerTemplateAction(
                        label="選取日期時間",
                        data="action=sell&mode=datetime",
                        mode="datetime",
                        initial="2021-06-01T10:00",
                        min="2021-01-01T00:00",
                        max="2021-12-31T23:59"
                        )
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤!"))
        


def sendData_sell(event, backdata):
    try:
        if backdata.get('mode') == 'date':
            dt = '日期為 : ' + event.postback.params.get('date')
        elif backdata.get('mode') == 'time':
            dt = '時間為 : ' + event.postback.params.get('time')
        elif backdata.get('mode') == 'datetime':
            dt = datetime.datetime.strptime(event.postback.params.get('datetime'), '%Y-%m-%dT%H:%M')
            dt = dt.strftime('{d}%Y-%m-%d, {t}%H:%M').format(d='日期為 : ', t='時間為 : ')
        message = TextSendMessage(
            text=dt
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
        

    
def sendFlex(event):
    try:
        bubble = BubbleContainer(
            direction='ltr',
            header=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='生活用品', weight='bold', size='xxl'),
                    ]
                ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    ImageComponent(
                        url='https://i.imgur.com/LAATyI5.jpg',
                        size='full',
                        aspect_ratio='400:400',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='毛毛蟲MINI熊寶寶', size='xl'),
                    BoxComponent(
                        layout='baseline',
                        margin='lg',
                        contents=[
                            TextComponent(text='價格 : $ 450', size='lg', color='#999999', flex=0),
                            ]
                        ),
                    ImageComponent(
                        url='https://i.imgur.com/2MNqIoQ.jpg',
                        size='full',
                        aspect_ratio='400:400',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='綠意女神餐食罐', size='xl'),
                    BoxComponent(
                        layout='baseline',
                        margin='lg',
                        contents=[
                            TextComponent(text='價格 : $ 1480', size='lg', color='#999999', flex=0),
                            ]
                        ),
                    ImageComponent(
                        url='https://i.imgur.com/mygoGyF.jpg',
                        size='full',
                        aspect_ratio='400:400',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='透黑NEW SIREN中禮袋提袋', size='xl'),
                    BoxComponent(
                        layout='baseline',
                        margin='lg',
                        contents=[
                            TextComponent(text='價格 : $ 600', size='lg', color='#999999', flex=0),
                            ]
                        ),
                    ImageComponent(
                        url='https://i.imgur.com/xh16Hoq.jpg',
                        size='full',
                        aspect_ratio='400:400',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='橄欖綠NEW SIREN中禮袋提袋', size='xl'),
                    BoxComponent(
                        layout='baseline',
                        margin='lg',
                        contents=[
                            TextComponent(text='價格 : $ 510', size='lg', color='#999999', flex=0),
                            ]
                        ),
                    ImageComponent(
                        url='https://i.imgur.com/VaOqfph.jpg',
                        size='full',
                        aspect_ratio='400:400',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='橄欖綠NEW SIREN 零錢包', size='xl'),
                    BoxComponent(
                        layout='baseline',
                        margin='lg',
                        contents=[
                            TextComponent(text='價格 : $ 400', size='lg', color='#999999', flex=0),
                            ]
                        )
                    

                    ],
                ),
            footer=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='Copyright@starbucks 2022', color='#888888', size='sm', align='center'),
                    ]
                ),
            )
        message = FlexSendMessage(alt_text="生活用品", contents=bubble)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))

    
    


def sendFlex1(event):
    try:
        bubble = BubbleContainer(
            direction='ltr',
            header=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='星巴克特殊門市', weight='bold', size='xxl'),
                    ]
                ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    ImageComponent(
                        url='https://i.imgur.com/nSKACWJ.jpg',
                        size='full',
                        aspect_ratio='792:555',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='洄瀾門市', size='xl', weight='bold'),
                    TextComponent(text='亞洲首間貨櫃屋門市', size='md'),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業地址:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text='花蓮縣吉安鄉南濱路一段 505 號', color='#666666', size='sm', flex=5),
                                    ],
                                ),
                            SeparatorComponent(color='#0000FF'),
                            ],
                        ),
                    BoxComponent(
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                color='#46A3FF',
                                height='sm',
                                action=URIAction(label='電話聯絡', uri='tel:03-8420014'),
                                ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='詳細介紹', uri="https://www.starbucks.com.tw/stores/special/stores_special_hualienbay.jspx")
                                )
                            ]
                        ),
                    
                    
                    TextComponent(text='\n\n\n', size='xl', weight='bold'),
                    ImageComponent(
                        url='https://i.imgur.com/PLJyNmn.jpg',
                        size='full',
                        aspect_ratio='792:555',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='草山門市', size='xl'),
                    TextComponent(text='1950年代美軍眷舍改建，今與昔在咖啡香中流轉', size='md'),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業地址:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text='台北市士林區國泰街5號', color='#666666', size='sm', flex=5),
                                    ],
                                ),
                            SeparatorComponent(color='#0000FF'),
                            ],
                        ),
                    BoxComponent(
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                color='#46A3FF',
                                height='sm',
                                action=URIAction(label='電話聯絡', uri='tel:02-28627317'),
                                ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='詳細介紹', uri="https://www.starbucks.com.tw/stores/special/stores_special_grass-mountain.jspx")
                                )
                            ]
                        ),
                    
                    
                    TextComponent(text='\n\n\n', size='xl', weight='bold'),
                    ImageComponent(
                        url='https://i.imgur.com/5mKipPx.jpg',
                        size='full',
                        aspect_ratio='792:555',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='天玉門市', size='xl'),
                    TextComponent(text='天母浪漫新地標，在林蔭包圍中喝咖啡', size='md'),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業地址:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text='台北市士林區天玉街 38 巷 18 弄 1 號', color='#666666', size='sm', flex=5),
                                    ],
                                ),
                            SeparatorComponent(color='#0000FF'),
                            ],
                        ),
                    BoxComponent(
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                color='#46A3FF',
                                height='sm',
                                action=URIAction(label='電話聯絡', uri='tel:02-28751361'),
                                ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='詳細介紹', uri="https://www.starbucks.com.tw/stores/special/stores_special_tianyu.jspx")
                                )
                            ]
                        ),
                    
                    
                    
                    TextComponent(text='\n\n\n', size='xl', weight='bold'),
                    ImageComponent(
                        url='https://i.imgur.com/CeZnjYP.jpg',
                        size='full',
                        aspect_ratio='792:555',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='淡水雲門門市', size='xl'),
                    TextComponent(text='劇場藝術與咖啡的相遇', size='md'),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業地址:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text='新北市淡水區中正路一段 6 巷 32-1 號', color='#666666', size='sm', flex=5),
                                    ],
                                ),
                            SeparatorComponent(color='#0000FF'),
                            ],
                        ),
                    BoxComponent(
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                color='#46A3FF',
                                height='sm',
                                action=URIAction(label='電話聯絡', uri='tel:02-28055247'),
                                ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='詳細介紹', uri="https://www.starbucks.com.tw/stores/special/stores_special_zhongzheng-tamsui.jspx")
                                )
                            ]
                        ),
                    
                    
                    
                    TextComponent(text='\n\n\n', size='xl', weight='bold'),
                    ImageComponent(
                        url='https://i.imgur.com/3D3Xo4o.jpg',
                        size='full',
                        aspect_ratio='792:555',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='馬祖門市', size='xl'),
                    TextComponent(text='最北端門市，展現馬祖島嶼魅力', size='md'),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業地址:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text='連江縣南竿鄉福沃村 8 鄰 143-1 號', color='#666666', size='sm', flex=5),
                                    ],
                                ),
                            SeparatorComponent(color='#0000FF'),
                            ],
                        ),
                    BoxComponent(
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                color='#46A3FF',
                                height='sm',
                                action=URIAction(label='電話聯絡', uri='tel:0836-22847'),
                                ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='詳細介紹', uri="https://www.starbucks.com.tw/stores/special/stores_special_nangan-matsu.jspx")
                                )
                            ]
                        ),
                    
                    
                    TextComponent(text='\n\n\n', size='xl', weight='bold'),
                    ImageComponent(
                        url='https://i.imgur.com/xPt9t6j.jpg',
                        size='full',
                        aspect_ratio='792:555',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='鹿港門市', size='xl'),
                    TextComponent(text='鹿港百年風華今與昔', size='md'),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業地址:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text='彰化縣鹿港鎮中正路 512 號', color='#666666', size='sm', flex=5),
                                    ],
                                ),
                            SeparatorComponent(color='#0000FF'),
                            ],
                        ),
                    BoxComponent(
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                color='#46A3FF',
                                height='sm',
                                action=URIAction(label='電話聯絡', uri='tel:04-7766277'),
                                ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='詳細介紹', uri="https://www.starbucks.com.tw/stores/special/stores_special_lukang.jspx")
                                )
                            ]
                        ),
                    
                    
                    
                    TextComponent(text='\n\n\n', size='xl', weight='bold'),
                    ImageComponent(
                        url='https://i.imgur.com/foCPZwB.jpg',
                        size='full',
                        aspect_ratio='792:555',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='澎湖喜來登門市', size='xl'),
                    TextComponent(text='澎湖海島風情咖啡印象', size='md'),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業地址:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text='澎湖縣馬公市新店路 197 號 1 樓', color='#666666', size='sm', flex=5),
                                    ],
                                ),
                            SeparatorComponent(color='#0000FF'),
                            ],
                        ),
                    BoxComponent(
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                color='#46A3FF',
                                height='sm',
                                action=URIAction(label='電話聯絡', uri='tel:06-9268509'),
                                ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='詳細介紹', uri="https://www.starbucks.com.tw/stores/special/stores_special_sheraton-magong.jspx")
                                )
                            ]
                        ),
                    
                    
                    
                    TextComponent(text='\n\n\n', size='xl', weight='bold'),
                    ImageComponent(
                        url='https://i.imgur.com/IEZ2YmG.jpg',
                        size='full',
                        aspect_ratio='792:555',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='內湖民權門市', size='xl'),
                    TextComponent(text='第一間綠建築門市，從內而外落實愛地球主張', size='md'),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業地址:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text='台北市內湖區民權東路六段 182 號', color='#666666', size='sm', flex=5),
                                    ],
                                ),
                            SeparatorComponent(color='#0000FF'),
                            ],
                        ),
                    BoxComponent(
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                color='#46A3FF',
                                height='sm',
                                action=URIAction(label='電話聯絡', uri='tel:02-2793-9550'),
                                ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='詳細介紹', uri="https://www.starbucks.com.tw/stores/special/stores_special_neihu-minquan.jspx")
                                )
                            ]
                        ),
                    
                    
                    
                    TextComponent(text='\n\n\n', size='xl', weight='bold'),
                    ImageComponent(
                        url='https://i.imgur.com/uaZiaOS.jpg',
                        size='full',
                        aspect_ratio='792:555',
                        aspect_mode='cover',
                        ),
                    TextComponent(text='嘉義民雄門市', size='xxl'),
                    TextComponent(text='咖啡風景連成一幅美麗的協奏曲', size='md'),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業地址:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text='嘉義縣民雄鄉建國路一段 235 號', color='#666666', size='sm', flex=5),
                                    ],
                                ),
                            SeparatorComponent(color='#0000FF'),
                            ],
                        ),
                    BoxComponent(
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                color='#46A3FF',
                                height='sm',
                                action=URIAction(label='電話聯絡', uri='tel:05-2268724'),
                                ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='詳細介紹', uri="https://www.starbucks.com.tw/stores/special/stores_special_minxiong-chiayi.jspx")
                                )
                            ]
                        )
                    
                    
                    
                    ],
                ),
            footer=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='Copyright@starbucks 2022', color='#888888', size='sm', align='center'),
                    ]
                ),
            )
        message = FlexSendMessage(alt_text="星巴克特殊門市", contents=bubble)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    