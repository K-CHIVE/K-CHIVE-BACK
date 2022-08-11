from django.urls import path
from .views import *

urlpatterns = [
    path('', GoodsListView.as_view()),
]