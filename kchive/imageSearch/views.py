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
from .models import GroupNotification
# Create your views here.

searched_id=[]



def extract(rawresults):
    global searched_id
    if 'extended_entities' in rawresults:
        searched_id.append(rawresults['id'])
        extractedresults={}
        extractedresults['user_name']=rawresults['entities']['user_mentions'][0]['name']
        extractedresults['user_screen_name']=rawresults['entities']['user_mentions'][0]['screen_name']
        extractedresults['created_at']=rawresults['created_at']
        extractedresults['retweet_count']=rawresults['retweeted_status']['retweet_count']
        extractedresults['in_reply_to_status_id']=rawresults['in_reply_to_status_id']
        extractedresults['favorite_count']=rawresults['retweeted_status']['favorite_count']
        extractedresults['meida_url']=rawresults['retweeted_status']['extended_entities']['media']
        return extractedresults
    else:
        return None#맞나

    #gif는 나중에 추가 file 로 되어있는지 media로 되어있는지 확인
    #사진을 누르면 해당 트윗으로 이동하게 url추가해야하나?

def extractnotification(rawresults):
    global searched_id
    if rawresults['retweeted_status']['full_text']:
        searched_id.append(rawresults['id'])
        extractedresults={}
        extractedresults['Group']=rawresults['entities']['user_mentions'][0]['name'] #해당 계정이 등록된 모델의 그룹이름으로 하는 것이 좋을까?
        extractedresults['Notification']=rawresults['retweeted_status']['full_text']

        return extractedresults
    else:
        return None

def extractfantweets(rawresults):
    for i in range(len(rawresults)):
        if rawresults[i]['id'] in searched_id:
            continue
        else:
            fantweetresult={}
            fantweetresult['user_name']=rawresults['entities']['user_mentions'][0]['name']
            fantweetresult['user_screen_name']=rawresults['entities']['user_mentions'][0]['screen_name']
            fantweetresult['created_at']=rawresults['created_at']
            fantweetresult['retweet_count']=rawresults['retweeted_status']['retweet_count']
            fantweetresult['in_reply_to_status_id']=rawresults['in_reply_to_status_id']
            fantweetresult['favorite_count']=rawresults['retweeted_status']['favorite_count']
            fantweetresult['full_text']=rawresults['retweeted_status']['full_text']

            return fantweetresult
        
    



class ContentsListView(APIView):
    
    def group_contentsearch(self, api, group_tag) :
        group_contentresults = []
        tweets = get_tweet_by_keyword(api, group_tag)

        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = extract(tweet._json)                    
                group_contentresults.append(tmp)


        return sorted(group_contentresults, key = lambda x : x['created_at'], reverse=True)
        #그룹의 그룹태그대로 트위터 서치하고 생성 날짜 내림차순으로 그룹멤버에 대한 트윗 리스트 반환
        #영민님께서 요청하신 사항에 대해서만 정리

    def member_contentsearch(self, api, member_tag) :
        print(member_tag)
        member_contentresults = []
        tweets = get_tweet_by_keyword(api, member_tag)

        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = extract(tweet._json)
                member_contentresults.append(tmp)     

        return sorted(member_contentresults, key = lambda x : x['created_at'], reverse=True)
        #멤버태그대로 트윗 서치하고 생성 날짜 내림차순으로 리스트반환

    # 필터 목록 (127.0.0.1:8000/food-search?group=그룹명&member=멤버명&search=검색어&startDate=시작날짜&endDate=종료날짜)
    def get(self, request) :
        api = connect_api()

        # 그룹은 무조건 있어야함 -> 일단 지금은 그룹 당 태그 하나로만 검색

        group = Group.objects.filter(name = self.request.query_params.get('group')).first()
        member = Member.objects.filter(group = group).filter(name = self.request.query_params.get('member')).first()
        #그룹,멤버 모델 안의 것들 필터로 url의 퀴어리 패럼에서 얻어서 해당하는 모델 member변수안에 저장
        if not group : 
            return HttpResponse(status = 400)
        
        if member and member.tag1 : 
            member_contentresults = self.member_contentsearch(api, member.tag1)
            return HttpResponse(status = 200, content=json.dumps(member_contentresults))

        else : 
            group_contentresults = self.group_contentsearch(api, group.tag1)
            return HttpResponse(status = 200, content=json.dumps(group_contentresults))

      
class GroupNotificationListView(APIView):
    
    def group_notificationsearch(self, api, group_tag) :
        group_notificationresults = []
        tweets = get_tweet_by_keyword(api, group_tag)

        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = extractnotification(tweet._json)                    
                group_notificationresults.append(tmp)


        return sorted(group_notificationresults, key = lambda x : x['created_at'], reverse=True)
        #그룹의 그룹태그대로 트위터 서치하고 생성 날짜 내림차순으로 그룹멤버에 대한 트윗 리스트 반환
        #영민님께서 요청하신 사항에 대해서만 정리 #나중에 확인!

    def member_notificationsearch(self, api, member_tag) :
        print(member_tag)
        member_notificationresults = []
        tweets = get_tweet_by_keyword(api, member_tag)

        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = extractnotification(tweet._json)
                member_notificationresults.append(tmp)     

        return sorted(member_notificationresults, key = lambda x : x['created_at'], reverse=True)
        #멤버태그대로 트윗 서치하고 생성 날짜 내림차순으로 리스트반환

    # 필터 목록 (127.0.0.1:8000/food-search?group=그룹명&member=멤버명&search=검색어&startDate=시작날짜&endDate=종료날짜)
    def get(self, request) :
        api = connect_api()

        # 그룹은 무조건 있어야함 -> 일단 지금은 그룹 당 태그 하나로만 검색

        groupnotification = GroupNotification.objects.filter(name = self.request.query_params.get('group')).first()
        #membernotification = Member.objects.filter(group = groupnotification).filter(name = self.request.query_params.get('member')).first()
        #그룹,멤버 모델 안의 것들 필터로 url의 퀴어리 패럼에서 얻어서 해당하는 모델 member변수안에 저장
        #멤버별로 
        if not groupnotification : 
            return HttpResponse(status = 400)
        

        else : 
            group_notificationresults = self.group_notificationsearch(api, groupnotification.refergroup)
            return HttpResponse(status = 200, content=json.dumps(group_notificationresults))
    
class FantweetListView(APIView) :

    def group_fantweetsearch(self, api, group_tag) :
        group_fantweetresults = []
        tweets = get_tweet_by_keyword(api, group_tag)

        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = extractfantweets(tweet._json)                    
                group_fantweetresults.append(tmp)     

        return sorted(group_fantweetresults, key = lambda x : x['created_at'], reverse=True)

    def member_fantweetsearch(self, api, member_tag) :
        print(member_tag)
        member_fantweetresults = []
        tweets = get_tweet_by_keyword(api, member_tag)

        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = extractfantweets(tweet._json)
                member_fantweetresults.append(tmp)     

        return sorted(member_fantweetresults, key = lambda x : x['created_at'], reverse=True)
   

    # 필터 목록 (127.0.0.1:8000/food-search?group=그룹명&member=멤버명&search=검색어&startDate=시작날짜&endDate=종료날짜)
    def get(self, request) :
        api = connect_api()

        # 그룹은 무조건 있어야함 -> 일단 지금은 그룹 당 태그 하나로만 검색

        group = Group.objects.filter(name = self.request.query_params.get('group')).first()
        member = Member.objects.filter(group = group).filter(name = self.request.query_params.get('member')).first()

        if not group : 
            return HttpResponse(status = 400)
        
        if member and member.tag1 : 
            member_results = self.member_fantweetsearch(api, member.tag1)
            return HttpResponse(status = 200, content=json.dumps(member_results))

        else : 
            group_results = self.group_fantweetsearch(api, group.tag1)
            return HttpResponse(status = 200, content=json.dumps(group_results))  
    

