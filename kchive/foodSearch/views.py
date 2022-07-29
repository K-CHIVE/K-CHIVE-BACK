from rest_framework.views import APIView
from .models import *
from django.conf import settings
import requests
import json
import tweepy

from django.http import HttpResponse

# Create your views here.

class RestaurantListView(APIView) :

    def get(self, request) :
        apiKey = getattr(settings, 'API_KEY', None)
        apiKeySecret = getattr(settings, 'API_KEY_SECRET', None)
        accessToken = getattr(settings, 'ACCESS_TOKEN', None)
        accessTokenSecret = getattr(settings, 'ACCESS_TOKEN_SECRET', None)

        # 트위터에 글 쓰기
        auth = tweepy.OAuthHandler(apiKey, apiKeySecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)
        api.update_status('예제를 작성해보십니다2')
        
        
        return HttpResponse(status = 200)