from django.urls import path
from goodsTransaction import views

urlpatterns = [
    path('', views.main, name="main"),
]