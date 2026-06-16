from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json
from .models import *

User = get_user_model()


def get_user_from_scope(scope):
    scope_user = scope.get('user')
    if not getattr(scope_user, 'is_authenticated', False):
        return None
    return User.objects.get(pk=scope_user.id)


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = get_user_from_scope(self.scope)
        if not self.user:
            self.close()
            return
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )
        self.accept()
        if self.chatroom.groupchat_name and self.user not in self.chatroom.members.all():
            self.chatroom.members.add(self.user)
        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

    def disconnect(self, close_code):
        if hasattr(self, 'chatroom_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.chatroom_name,
                self.channel_name
            )
        if hasattr(self, 'chatroom') and self.user:
            if self.user in self.chatroom.users_online.all():
                self.chatroom.users_online.remove(self.user)
                self.update_online_count()


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

    def update_online_count(self):
        online_count = self.chatroom.users_online.count() - 1
        event = {
            'type': 'online_count_handler',
            'online_count': online_count,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )    
    def online_count_handler(self, event):
        online_count = event['online_count']
        html = render_to_string(
            'a_rtchat/partials/online_count_p.html',
            context={
                'online_count': online_count,
                'chat_group': self.chatroom,
            }
        )
        self.send(text_data=html)    


class OnlineStatusConsumer(WebsocketConsumer):
    def connect(self):
        self.user = get_user_from_scope(self.scope)
        if not self.user:
            self.close()
            return
        self.group_name = 'online-status'
        self.group, _ = ChatGroup.objects.get_or_create(group_name=self.group_name)
        
        if self.user not in self.group.users_online.all():
            self.group.users_online.add(self.user)
            
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        
        self.accept()
        self.online_status()
        
        
    def disconnect(self, close_code):
        if self.user and hasattr(self, 'group') and self.user in self.group.users_online.all():
            self.group.users_online.remove(self.user)
            
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name, self.channel_name
            )
        if hasattr(self, 'group'):
            self.online_status()
        
        
    def online_status(self):
        event = {
            'type': 'online_status_handler'
        }
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, event
        ) 
        
    def online_status_handler(self, event):
        online_users = self.group.users_online.all()
        other_online_users = self.group.users_online.exclude(id=self.user.id)
        public_chat = ChatGroup.objects.filter(group_name='public-chat').first()
        public_chat_users = public_chat.users_online.exclude(id=self.user.id).exists() if public_chat else False
        
        my_chats = self.user.chat_groups.all()
        private_chats_with_users = [chat for chat in my_chats.filter(is_private=True) if chat.users_online.exclude(id=self.user.id).exists()]
        group_chats_with_users = [chat for chat in my_chats.filter(groupchat_name__isnull=False) if chat.users_online.exclude(id=self.user.id).exists()]
        
        if public_chat_users or private_chats_with_users or group_chats_with_users:
            online_in_chats = True
        else:
            online_in_chats = False
        
        context = {
            'online_users': online_users,
            'other_online_users': other_online_users,
            'online_in_chats': online_in_chats,
            'public_chat_users': public_chat_users,
            'user': self.user
        }
        html = render_to_string("a_rtchat/partials/online_status.html", context=context)
        self.send(text_data=html) 