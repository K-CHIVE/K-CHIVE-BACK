from rest_framework.views import APIView
from .models import *
from django.conf import settings
import requests
import json
import tweepy
from pprint import pprint

from django.http import HttpResponse

# Create your views here.

class RestaurantListView(APIView) :

    # 공통으로 사용할 수 있을듯, 프로젝트명 레포에 utils.py를 만들어서 트위터 API관련 함수들을 모아두기
    def connect_api(self) :
        apiKey = getattr(settings, 'API_KEY', None)
        apiKeySecret = getattr(settings, 'API_KEY_SECRET', None)
        accessToken = getattr(settings, 'ACCESS_TOKEN', None)
        accessTokenSecret = getattr(settings, 'ACCESS_TOKEN_SECRET', None)

        # 트위터에 접근하기
        auth = tweepy.OAuthHandler(apiKey, apiKeySecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        return api

    def get_tweet_by_keyword(self, api, keyword) :
        cursor = tweepy.Cursor(api.search_tweets, keyword, tweet_mode = 'extended')
        return cursor.items()


    # GET 요청 시 params로 필터 처리해야함 
    # 필터 목록 (127.0.0.1:8000/food-search?group=그룹명&member=멤버명&search=검색어&startDate=시작날짜&endDate=종료날짜)
    def get(self, request) :
        api = self.connect_api()
        keyword = "#블랙핑크_맛집사거리"
        apiResult = self.get_tweet_by_keyword(api, keyword)
        print("검색 성공")
        tweets = []

        for i, tweet in enumerate(apiResult):
            tweets.append(tweet._json)

        # pprint(tweets[0]['retweeted_status']) # 글 세부정보
        # pprint(tweets[0]['user']) # 작성자 세부정보

        pprint(tweets[0]['retweeted_status']['created_at'])
        pprint(tweets[0]['retweeted_status']['full_text'])
        pprint(tweets[0]['retweeted_status']['entities']['hashtags'])

        # 해야할 일
        # 게시글 url, 미디어 url, 작성자 정보 반환
        # Region Model을 만들어서 
        # 홍대, 신촌, 압구정 등 키워드를 찾은 뒤 지역 필터를 실행
        
        
        return HttpResponse(status = 200)   