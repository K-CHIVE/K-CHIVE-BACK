from rest_framework.views import APIView
from common.models import *
import json
from django.http import HttpResponse
from common.views import connect_api, get_tweet_by_keyword
from .models import GroupNotification
from .functions import *
# Create your views here.

class ContentsListView(APIView):
    
    def group_contentsearch(self, api, group_tag) :
        group_contentresults = []
        tweets = get_tweet_by_keyword(api, group_tag)

        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = extract(tweet._json)                    
                group_contentresults.append(tmp)

        return sorted(group_contentresults, key = lambda x : x['created_at'], reverse=True)
        #그룹의 그룹 태그대로 트위터 서치하고 생성 날짜 내림차순으로 그룹태그에 대한 트윗 리스트 반환

    def member_contentsearch(self, api, member_tag) :
        print(member_tag)
        member_contentresults = []
        tweets = get_tweet_by_keyword(api, member_tag)

        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = extract(tweet._json)
                member_contentresults.append(tmp)     

        return sorted(member_contentresults, key = lambda x : x['created_at'], reverse=True)
        #그룹의 그룹 태그대로 트위터 서치하고 생성 날짜 내림차순으로 그룹태그에 대한 트윗 리스트 반환

    # 필터 목록 (127.0.0.1:8000/image-search/contents/?group=그룹명&member=멤버명&startDate=시작날짜(여섯자리 ex)220819)&endDate=종료날짜(여섯자리 ex)220819))
    def get(self, request) :
        api = connect_api()

        # 그룹은 무조건 있어야함 -> 일단 지금은 그룹 당 태그 하나로만 검색
        group = Group.objects.filter(name = self.request.query_params.get('group')).first()
        member = Member.objects.filter(group = group).filter(name = self.request.query_params.get('member')).first()
        startdate=self.request.query_params.get('startDate')
        enddate=self.request.query_params.get('endDate')
        #그룹,멤버는 모델 참조해서 url의 패럼에 있는 것을 얻음(태그는 일단 첫번째것으로)
        if not group : 
            
            return HttpResponse(status = 400)
        #등록되지 않은 그룹이면 400반환
        
        if member and member.tag1 : 
            member_contentresults = self.member_contentsearch(api, member.tag1)
            member_contentresults=filtered_by_daterange(startdate,enddate,member_contentresults)

            return HttpResponse(status = 200, content=json.dumps(member_contentresults))
        #멤버가 있고 멤버태그가 있다면 멤버 콘텐츠서치해줌. 서치한 트윗들로 구성된 리스트들 반환하고 다시 날짜에 적합한 것으로 반환
        else : 
            group_contentresults = self.group_contentsearch(api, group.tag1)
            group_contentresults=filtered_by_daterange(startdate,enddate,group_contentresults)
            return HttpResponse(status = 200, content=json.dumps(group_contentresults))
        #멤버 없으면 그냥 그룹단위 콘텐츠서치해줌. 서치한 트윗들로 구성된 리스트들 반환하고 다시 날짜에 적합한 것으로 반환

      
class GroupNotificationListView(APIView):
    
    def group_notificationsearch(self, api, officialid) :
        group_notificationresults = []
        tweets = get_timeline_by_id(api, officialid)
        
        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                tmp = extractnotification(tweet._json)                    
                group_notificationresults.append(tmp)

        return sorted(group_notificationresults, key = lambda x : x['created_at'], reverse=True)
        #계정 입력하면 타임라인 긁어올 수 있는 함수

    # def member_notificationsearch(self, api, member_tag) :
    #     print(member_tag)
    #     member_notificationresults = []
    #     tweets = get_tweet_by_keyword(api, member_tag)

    #     for i, tweet in enumerate(tweets) :
    #         if 'retweeted_status' in tweet._json : 
    #             tmp = extractnotification(tweet._json)
    #             member_notificationresults.append(tmp)     

    #     return sorted(member_notificationresults, key = lambda x : x['created_at'], reverse=True)
        #멤버태그대로 트윗 서치하고 생성 날짜 내림차순으로 리스트반환

    # 필터 목록 (127.0.0.1:8000/image-search/groupnotifications/group=그룹명&startDate=시작날짜(여섯자리 ex)220819)&endDate=종료날짜(여섯자리 ex)220819))
    def get(self, request) :
        api = connect_api()
        groupnotification = GroupNotification.objects.filter(refergroup = self.request.query_params.get('group')).first()
        startdate=self.request.query_params.get('startDate')
        enddate=self.request.query_params.get('endDate')
        #membernotification = Member.objects.filter(group = groupnotification).filter(name = self.request.query_params.get('member')).first()

        if not groupnotification : 
            return HttpResponse(status = 400)
        
        else : 
            group_notificationresults = self.group_notificationsearch(api, groupnotification.refergroup)
            group_notificationresults=filtered_by_daterange(startdate,enddate,group_notificationresults)
            return HttpResponse(status = 200, content=json.dumps(group_notificationresults))
    
class FantweetListView(APIView) :

    def group_fantweetsearch(self, api, group_tag,searchtype) :
        group_fantweetresults = []
        tweets = get_tweet_by_keyword(api, group_tag)
        
        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                if searchtype=='fulltext':
                    tmp = extractfantweetsfulltext(tweet._json)
                    group_fantweetresults.append(tmp) 

                if searchtype=='onlyhashtag':
                    tmp = extractfantweetsonlyhastag(tweet._json)
                    group_fantweetresults.append(tmp) 

                if searchtype=='withouthastag':
                    tmp = extractfantweetswithouthastag(tweet._json)
                    group_fantweetresults.append(tmp) 
        return sorted(group_fantweetresults, key = lambda x : x['created_at'], reverse=True)

    def member_fantweetsearch(self, api, member_tag,searchtype) :
        member_fantweetresults = []
        tweets = get_tweet_by_keyword(api, member_tag)
        for i, tweet in enumerate(tweets) :
            if 'retweeted_status' in tweet._json : 
                if searchtype=='fulltext':
                    tmp = extractfantweetsfulltext(tweet._json)
                    member_fantweetresults.append(tmp) 

                if searchtype=='onlyhashtag':
                    tmp = extractfantweetsonlyhastag(tweet._json)
                    member_fantweetresults.append(tmp) 

                if searchtype=='withouthashtag':
                    tmp = extractfantweetswithouthastag(tweet._json)
                    member_fantweetresults.append(tmp) 
        return sorted(member_fantweetresults, key = lambda x : x['created_at'], reverse=True)
   

    # 필터 목록 (127.0.0.1:8000/image-search?group=그룹명&member=멤버명&searchtype=검색형식&startDate=시작날짜&endDate=종료날짜)
    def get(self, request) :
        api = connect_api()

        # 그룹은 무조건 있어야함 -> 일단 지금은 그룹 당 태그 하나로만 검색
        group = Group.objects.filter(name = self.request.query_params.get('group')).first()
        member = Member.objects.filter(group = group).filter(name = self.request.query_params.get('member')).first()
        searchtype=self.request.query_params.get('searchtype')
        startdate=self.request.query_params.get('startDate')
        enddate=self.request.query_params.get('endDate')

        if not group : 
            return HttpResponse(status = 400)
        
        if member and member.tag1 : 
            member_results = self.member_fantweetsearch(api, member.tag1,searchtype)
            member_results=filtered_by_daterange(startdate,enddate,member_results)
            return HttpResponse(status = 200, content=json.dumps(member_results))

        else : 
            group_results = self.group_fantweetsearch(api, group.tag1,searchtype)
            group_results=filtered_by_daterange(startdate,enddate,group_results)
            return HttpResponse(status = 200, content=json.dumps(group_results)) 
    

