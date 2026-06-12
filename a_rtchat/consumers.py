from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json
from .models import *

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )
        
        # Send user join event
        event = {
            'type': 'user_join',
            'username': self.user.username,
            'user_id': self.user.id,
            'avatar': self.user.avatar,
            'displayname': self.user.displayname or self.user.username,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )


    def receive(self, text_data):
        text_data_json = json.loads(text_data)    
        body = text_data_json['body']
        message = groupMessage.objects.create(
            group=self.chatroom,
            author=self.user,
            body=body
        )
        
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = groupMessage.objects.get(id=message_id)
        context = {
            'message' : message,
            'user' : self.user,
        }
        html = render_to_string('a_rtchat/partials/chat_message_p.html', context=context)
        self.send(text_data=html)
    
    def user_join(self, event):
        self.send(text_data=json.dumps({
            'type': 'user_join',
            'username': event['username'],
            'user_id': event['user_id'],
            'avatar': event['avatar'],
            'displayname': event['displayname'],
        }))   