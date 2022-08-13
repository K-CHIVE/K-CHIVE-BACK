from django.urls import path
from .views import *

urlpatterns = [
    # path('group',  groupInfo),
    path('group', GroupListView.as_view()),
    path('member', MemberListView.as_view()),
]