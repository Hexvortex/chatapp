import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import datetime
import random

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.random_number = str(random.randint(0,22))
        #Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
     
        )
        await self.accept()

    async def dissconnect(self,close_code):
        #Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        data = 'Anonymous:'+ self.random_number + " "+  message
        # now = datetime.datetime.now()
        #Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat_message',
                'message':data,
                # 'time':now
            }
        )

    async def chat_message(self,event):
        message = event['message']
        # time = event['time']

        #send message to websocket
        await self.send(text_data=json.dumps({
            'message':message,
            # 'time':time

        }))


