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
from common.views import connect_api, get_tweet_by_keyword, parse_tweet_response
# Create your views here.
    
class RestaurantListView(APIView) :

    def group_search(self, api, group_tag) :
        group_results = []
        tweets = get_tweet_by_keyword(api, group_tag)

        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = parse_tweet_response(tweet._json)                    
                group_results.append(tmp)     

        return sorted(group_results, key = lambda x : x['created_at'], reverse=True)

    def member_search(self, api, member_tag) :
        member_results = []
        tweets = get_tweet_by_keyword(api, member_tag)

        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = parse_tweet_response(tweet._json)
                member_results.append(tmp)     
        return sorted(member_results, key = lambda x : x['created_at'], reverse=True)

    def keyword_search(self, api, current_tag, keyword) :
        keyword_results = []
        print('keyword', keyword, current_tag)
        new_keyword = current_tag + str(keyword)
        tweets = get_tweet_by_keyword(api, new_keyword)

        for i, tweet in enumerate(tweets) : 
            if 'retweeted_status' in tweet._json : 
                tmp = parse_tweet_response(tweet._json)
                keyword_results.append(tmp)     
        return sorted(keyword_results, key = lambda x : x['created_at'], reverse=True)

    # 필터 목록 (127.0.0.1:8000/food-search?group=그룹명&member=멤버명&search=검색어&startDate=시작날짜&endDate=종료날짜)
    def get(self, request) :
        api = connect_api()

        # 그룹은 무조건 있어야함 -> 일단 지금은 그룹 당 태그 하나로만 검색
        group = Group.objects.filter(name = self.request.query_params.get('group')).first()
        member = Member.objects.filter(group = group).filter(name = self.request.query_params.get('member')).first()
        search = self.request.query_params.get('search')

        
        if member and member.tag1 : 
            if search : 
                keyword = member.tag1 + " " + str(search)
            else :
                keyword = member.tag1
            member_results = self.member_search(api, keyword)
            return HttpResponse(status = 200, content=json.dumps(member_results))


        else : 
            if search : 
                keyword = group.tag1 + " " + str(search)
            else : 
                keyword = group.tag1
            group_results = self.group_search(api, keyword)
            return HttpResponse(status = 200, content=json.dumps(group_results))  


        

        # 해야할 일
        # 홍대, 신촌, 압구정 등 키워드를 찾은 뒤 지역 필터를 실행
        # 카페 or 식당 -> 이게 근데 가능해 ?
        # 날짜 => 이건 안할꺼야
