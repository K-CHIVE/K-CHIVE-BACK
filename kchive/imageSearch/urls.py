from django.urls import path
from .views import *

urlpatterns = [
    path('contents/', ContentsListView.as_view()),
    path('groupnotifications/', GroupNotificationListView.as_view()),
    path('fantweets', FantweetListView.as_view()),

    
]