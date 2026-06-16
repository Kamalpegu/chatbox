from django.db import models
from django.conf import settings
import shortuuid
from PIL import Image
import os

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True, blank=True)
    groupchat_name = models.CharField(max_length=128, null=True, blank=True)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='groupchats', blank=True, null=True, on_delete=models.SET_NULL)
    users_online = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='online_in_groups', blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return self.group_name

    def save(self, *args, **kwargs):
        if not self.group_name:
            self.group_name = shortuuid.uuid()
        super().save(*args, **kwargs)
    
    
class groupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField(max_length=300, blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def filename(self):
        if self.file:
            return os.path.basename(self.file.name)
        else:
            return None

    @property
    def extension(self):
        if self.filename:
            return os.path.splitext(self.filename)[1].lower().lstrip('.')
        return ''

    @property
    def file_label(self):
        ext = self.extension.upper()
        if ext == 'PDF':
            return 'PDF'
        if ext in ['JPG', 'JPEG', 'PNG', 'GIF', 'WEBP']:
            return 'Image'
        if ext in ['MP4', 'MOV', 'WEBM']:
            return 'Video'
        if ext in ['MP3', 'WAV', 'OGG']:
            return 'Audio'
        if ext:
            return ext
        return 'File'
    
    def __str__(self):
        if self.body:
            return f'{self.author.username} : {self.body}'
        elif self.file:
            return f'{self.author.username} : {self.filename}'
    
    class Meta:
        ordering = ['-created']
        
    @property    
    def is_image(self):
        try:
            image = Image.open(self.file) 
            image.verify()
            return True 
        except:
            return False