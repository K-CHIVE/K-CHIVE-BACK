from django.contrib import admin
from .models import *

# Register your models here.

class GroupAdmin(admin.ModelAdmin) :
    list_display = ('id', 'name', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5',)

class MemberAdmin(admin.ModelAdmin) :
    list_display = ('id', 'group', 'name', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5',)


admin.site.register(Group, GroupAdmin)
admin.site.register(Member, MemberAdmin)