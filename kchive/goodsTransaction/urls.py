from django.urls import path
from .views import *

urlpatterns = [
    path('/goods', GoodsListView.as_view()),
    # path('/poca', GoodsListView.as_view()),
    # path('/album', GoodsListView.as_view()),
]