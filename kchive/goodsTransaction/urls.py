from django.urls import path
from .views import *

urlpatterns = [
    path('goods/', GoodsListView.as_view()),
    path('poca/', PocasListView.as_view()),
    path('album/', AlbumsListView.as_view()),
]
