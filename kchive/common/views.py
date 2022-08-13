# import sys
# sys.path.append('C:/Users/wuchi/likelion/K-CHIVE-BACK/myvenv/Lib')
# sys.path.append('C:/Users/wuchi/likelion/K-CHIVE-BACK/kchive/common')
from enum import EnumMeta
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.conf import settings
from rest_framework import viewsets
from django.http import HttpResponse
from datetime import date
import tweepy
import json

# 그룹 리스트 반환
class GroupListView(APIView) : 
    def get(self, request) : 
        groups = Group.objects.all()
        res = []

        for i, v in enumerate(groups) : 
            temp = {}
            temp['idx'] = i
            temp['name'] = v.name
            res.append(temp)

        return HttpResponse(status=200, content=json.dumps(res))


# 그룹별 멤버 리스트 반환
class MemberListView(APIView) : 
    def get(self, request) :
        groupName = self.request.query_params.get('group')

        if not groupName : 
            return HttpResponse(status=400)

        group = Group.objects.filter(name = groupName).first()
        members = Member.objects.filter(group = group)
        res = []

        for i, v in enumerate(members) : 
            temp = {}
            temp['idx'] = i + 1
            temp['name'] = v.name
            res.append(temp)
            
        return HttpResponse(status=200, content=json.dumps(res))

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

# 트위터 response 전처리하는 함수
def parse_tweet_response(info) : 
    tmp = {}
    tmp['id'] = info['id']
    tmp['created_at'] = info['created_at']
    hashtags = info['retweeted_status']['entities']['hashtags']
    tmp['hashtags'] = [hashtag['text'] for hashtag in hashtags]
    tmp['full_text'] = info['retweeted_status']['full_text']

    # url 다시 찾아야함 원본 게시글 url
    tmp['tweet_url'] = tmp['full_text'][tmp['full_text'].find('http'):]
    tmp['retweet_count'] = info['retweeted_status']['retweet_count']
    tmp['favorite_count'] = info['retweeted_status']['favorite_count']
    # tmp['user_name'] = info['user']['name']
    tmp['user_screen_name'] = info['entities']['user_mentions'][0]['screen_name']
    tmp['user_name'] = info['entities']['user_mentions'][0]['name']
    tmp['user_profile_image_url'] = info['user']['profile_image_url']

    if 'extended_entities' in info :
        medias = info['retweeted_status']['extended_entities']['media']
        tmp['media_url'] = [media['media_url'] for media in medias]
    else :
        tmp['media_url'] = None

    return tmp