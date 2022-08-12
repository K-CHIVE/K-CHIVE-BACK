from django.urls import path
from .views import *


groupInfo = GroupViewSet.as_view({
    'get' : 'list',
})

memberInfo = MemberViewSet.as_view({
    'get' : 'list',
})

urlpatterns = [
    path('group',  groupInfo),
    path('member', memberInfo),
]