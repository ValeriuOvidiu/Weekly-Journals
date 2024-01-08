
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import FriendsRequestModel


class FriendRequestConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]
   
    async def connect(self):
        self.room_name = str(self.scope["url_route"]["kwargs"]["id"])
        self.room_group_name = f"notification_{self.room_name}"
        print(self.room_group_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
        
    async def receive(self, text_data=None, bytes_data=None):  
        # Called with either text_data or bytes_data for each frame
        # You can call:
        print('alea se primeste', text_data)
        decoded_data = json.loads(text_data)
        self.other_user_username = decoded_data["username"]
        self.other_user , self.uread_notf = await self.get_name()
        self.channel_name= str(self.other_user.id )    
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": str(self.uread_notf)}
        )       
   
    @database_sync_to_async
    def get_name(self):  
        username=self.other_user_username   
        other_user=User.objects.get(username=username)
        user=self.scope["user"]
        unread_notf=(FriendsRequestModel.objects.filter(receiver=other_user).filter(request_seen=False)|FriendsRequestModel.objects.filter(sender=other_user).filter(accepted_seen=False)).count()
        return user,unread_notf

    async def disconnect(self, close_code):
       print('websocket disconected')
    
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))