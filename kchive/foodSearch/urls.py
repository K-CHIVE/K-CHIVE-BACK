from django.urls import path
from .views import *

urlpatterns = [
    path('', RestaurantListView.as_view()),
]