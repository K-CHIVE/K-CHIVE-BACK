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

class ContentsListView(APIView):
    
    def group_search(self, api, group_tag) :
        group_results = []
        tweets = get_tweet_by_keyword(api, group_tag)

        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = parse_tweet_response(tweet._json)                    
                group_results.append(tmp)     

        return sorted(group_results, key = lambda x : x['created_at'], reverse=True)
        #그룹의 그룹태그대로 트위터 서치하고 생성 날짜 내림차순으로 그룹멤버에 대한 트윗 리스트 반환

    def member_search(self, api, member_tag) :
        print(member_tag)
        member_results = []
        tweets = get_tweet_by_keyword(api, member_tag)

        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = parse_tweet_response(tweet._json)
                member_results.append(tmp)     

        return sorted(member_results, key = lambda x : x['created_at'], reverse=True)
        #멤버태그대로 트윗 서치하고 생성 날짜 내림차순으로 리스트반환

    # 필터 목록 (127.0.0.1:8000/food-search?group=그룹명&member=멤버명&search=검색어&startDate=시작날짜&endDate=종료날짜)
    def get(self, request) :
        api = connect_api()

        # 그룹은 무조건 있어야함 -> 일단 지금은 그룹 당 태그 하나로만 검색

        group = Group.objects.filter(name = self.request.query_params.get('group')).first()
        member = Member.objects.filter(group = group).filter(name = self.request.query_params.get('member')).first()

        if not group : 
            return HttpResponse(status = 400)
        
        if member and member.tag1 : 
            member_results = self.member_search(api, member.tag1)
            return HttpResponse(status = 200, content=json.dumps(member_results))

        else : 
            group_results = self.group_search(api, group.tag1)
            return HttpResponse(status = 200, content=json.dumps(group_results))  