from importlib.resources import contents
from django.contrib import admin
from .models import *
# Register your models here.

class ContentsAdmin(admin.ModelAdmin) :
    list_display = ('id', 'author', 'date', 'retweets', 'replies', 'hearts', 'group',)

class NoticesAdmin(admin.ModelAdmin) :
    list_display = ('id', 'author', 'notices',)

class FanTweetsAdmin(admin.ModelAdmin) :
    list_display = ('id', 'author', 'date', 'retweets', 'replies', 'hearts', 'group',)

admin.site.register(Content,ContentsAdmin)
admin.site.register(Notice,NoticesAdmin)
admin.site.register(Fantweet,FanTweetsAdmin)