from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True) 

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    @property
    def name(self):
        if self.displayname:
            name = self.displayname
        else:
            name = self.username 
        return name
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/avatar.svg')
        return avatar


class AuthUserProxy(CustomUser):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
