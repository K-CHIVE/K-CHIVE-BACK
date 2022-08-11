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

    # group으로만
    def group_search(self, api, group_tag) :
        group_results = []
        tweets = get_tweet_by_keyword(api, group_tag)

        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = {}
                tmp['id'] = tweet._json['id']
                tmp['created_at'] = tweet._json['created_at']
                hashtags = tweet._json['retweeted_status']['entities']['hashtags']
                tmp['hashtags'] = [hashtag['text'] for hashtag in hashtags]
                tmp['full_text'] = tweet._json['retweeted_status']['full_text']
                tmp['tweet_url'] = tmp['full_text'][tmp['full_text'].find('http'):]
                tmp['retweet_count'] = tweet._json['retweeted_status']['retweet_count']
                tmp['favorite_count'] = tweet._json['retweeted_status']['favorite_count']
                # tmp['user_name'] = tweet._json['user']['name']
                tmp['user_screen_name'] = tweet._json['entities']['user_mentions'][0]['screen_name']
                tmp['user_name'] = tweet._json['entities']['user_mentions'][0]['name']
                tmp['user_profile_image_url'] = tweet._json['user']['profile_image_url']

                if 'extended_entities' in tweet._json :
                    medias = tweet._json['retweeted_status']['extended_entities']['media']
                    tmp['media_url'] = [media['media_url'] for media in medias]
                else :
                    tmp['media_url'] = None
                    
                group_results.append(tmp)     

        return sorted(group_results, key = lambda x : x['created_at'], reverse=True)

    def member_search(self, api, member_tag) :
        member_results = []
        return member_results

    # member도
    # GET 요청 시 params로 필터 처리해야함 
    # 필터 목록 (127.0.0.1:8000/food-search?group=그룹명&member=멤버명&search=검색어&startDate=시작날짜&endDate=종료날짜)
    def get(self, request) :
        api = connect_api()

        # 그룹은 무조건 있어야함 -> 일단 지금은 그룹 당 태그 하나로만 검색
        group = Group.objects.filter(name = self.request.query_params.get('group')).first()
        member = Member.objects.filter(group = group).filter(name = self.request.query_params.get('member')).first()

        if not group : 
            return HttpResponse(status = 400)

        if not member : 
            group_results = self.group_search(api, group.tag1)
            return HttpResponse(status = 200, content=json.dumps(group_results))  
        
        if member.tag1 : 
            member_results = self.member_serach(api, member.tag1)
            return HttpResponse(status = 200, content=json.dumps(member_results))

        

        # 해야할 일
        # 홍대, 신촌, 압구정 등 키워드를 찾은 뒤 지역 필터를 실행
        # 멤버 필터
        # 날짜
