from django.urls import path
from goodsTransaction import views

urlpatterns = [
    path('goods/', GoodsListView.as_view()),
    # path('poca/', GoodsListView.as_view()),
    # path('album/', GoodsListView.as_view()),
]