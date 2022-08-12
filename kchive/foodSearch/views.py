#import os
#os.environ.setdefault('DJANGO_SETTINGS_MODULE','kchive.settings')

from ast import keyword
from rest_framework.views import APIView
from common.models import *
from django.conf import settings
import requests
import json
from pprint import pprint
from rest_framework import viewsets
from django.http import HttpResponse
from datetime import date
from common.views import connect_api, get_tweet_by_keyword
# Create your views here.

    
class RestaurantListView(APIView) :
    # GET 요청 시 params로 필터 처리해야함 
    # 필터 목록 (127.0.0.1:8000/food-search?group=그룹명&member=멤버명&search=검색어&startDate=시작날짜&endDate=종료날짜)
    def get(self, request) :
        api = connect_api()
    
        # 그룹은 무조건 있어야함
        group = Group.objects.filter(name = self.request.query_params.get('group')).first()
        api_results = []

        if group : 
            apiResult = get_tweet_by_keyword(api, group.tag1)
            for i, tweet in enumerate(apiResult) :
                if 'retweeted_status' in tweet._json : 
                    tmp = {}
                    tmp['created_at'] = tweet._json['retweeted_status']['created_at']
                    hashtags = tweet._json['retweeted_status']['entities']['hashtags']
                    tmp['hashtags'] = [hashtag['text'] for hashtag in hashtags]
                    tmp['full_text'] = tweet._json['retweeted_status']['full_text']
                    tmp['retweet_count'] = tweet._json['retweeted_status']['retweet_count']
                    tmp['favorite_count'] = tweet._json['retweeted_status']['favorite_count']
                    tmp['user_id'] = tweet._json['user']['id']
                    tmp['user_name'] = tweet._json['user']['name']
                    tmp['user_profile_image_url'] = tweet._json['user']['profile_image_url']

                    if 'extended_entities' in tweet._json :
                        tmp['tweet_url'] = tweet._json['retweeted_status']['extended_entities']['media'][0]['expanded_url']
                        tmp['media_url'] = tweet._json['retweeted_status']['extended_entities']['media'][0]['media_url']
                    api_results.append(tmp)            

            api_results = sorted(api_results, key = lambda x : x['created_at'], reverse=True)
            return HttpResponse(status = 200, content=json.dumps(api_results))  
        
        else :
            return HttpResponse(status = 400)

        # 해야할 일
        # 홍대, 신촌, 압구정 등 키워드를 찾은 뒤 지역 필터를 실행
