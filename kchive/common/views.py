# import sys
# sys.path.append('C:/Users/wuchi/likelion/K-CHIVE-BACK/myvenv/Lib')
# sys.path.append('C:/Users/wuchi/likelion/K-CHIVE-BACK/kchive/common')
from .models import *
from .serializers import *
from django.conf import settings
from rest_framework import viewsets
from django.http import HttpResponse
from datetime import date
import tweepy

# 그룹 리스트 반환
class GroupViewSet(viewsets.ModelViewSet) :
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# 그룹별 멤버 리스트 반환 : 
class MemberViewSet(viewsets.ModelViewSet) :
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        group = Group.objects.filter(name = self.request.query_params.get('group')).first()
        return qs.filter(group = group)

# 공통으로 사용할 수 있을듯, 프로젝트명 레포에 utils.py를 만들어서 트위터 API관련 함수들을 모아두기
def connect_api() :
    apiKey = getattr(settings, 'API_KEY', None)
    apiKeySecret = getattr(settings, 'API_KEY_SECRET', None)
    accessToken = getattr(settings, 'ACCESS_TOKEN', None)
    accessTokenSecret = getattr(settings, 'ACCESS_TOKEN_SECRET', None)

    # 트위터에 접근하기
    auth = tweepy.OAuthHandler(apiKey, apiKeySecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api

def get_tweet_by_keyword(api, keyword) :
    cursor = tweepy.Cursor(api.search_tweets, keyword, tweet_mode = 'extended')
    return cursor.items()
