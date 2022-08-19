from ast import keyword
from asyncio.format_helpers import extract_stack
from posixpath import split
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
import tweepy

# searched_id=[]
#daterangefilter
def datetonumber(date):
    Dow,Month,Date,Time,Nation,Year=date.split()
    MonthEng=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    MonthEngDict={}
    
    for i,v in enumerate(MonthEng):
        MonthEngDict[v]='%02d'%(i+1)
    
    EngMonthinNum=MonthEngDict[Month]
    DateintoNumber=Year[-1]+Year[-2]+EngMonthinNum+Date
    
    return DateintoNumber
    #createdat날짜형식을 6자리수로 바꿔줌

def filter_by_daterange(startdate,enddate,objectdict):
    time=int(datetonumber(objectdict['created_at']))

    if time>=int(startdate) and time<=int(enddate):
        
        return objectdict
    
    else:
        
        return None
    #트윗하나가 해당 날짜 안에 들어있는지 확인하고 조건이 충족하면 반환해줌
#searchtypefilter(hashtag)
def text_without_hashtag(rawresult):
    fulltext=rawresult['full_text'].replace(rawresult['retweeted_status']['extended_entities']['media'][0]['url'],'')
    hashtags=rawresult['retweeted_status']['entities']['hashtags']
    textwithouthashtag=fulltext
    
    for i in range(len(hashtags)):

        textwithouthashtag=textwithouthashtag.replace('#'+hashtags[i]['text'],'')
    
    return textwithouthashtag
#원본 트윗(하나)을 넘겨주면 해시태그 없는 본문을 반환함

def filtered_by_daterange(startdate,enddate,objects):
    resultsfilteredbydaterange=[]
    
    for i in range(len(objects)):
        resultsfilteredbydaterange.append(filter_by_daterange(startdate,enddate,objects[i]))
    
    return resultsfilteredbydaterange
#트윗들로 이루어진 리스트들 전체를 날짜내에 있는지 확인하고 걸러서 트윗들로 이루어진 리스트 반환

#contentssearch
def extract(rawresult):
    extractedresult={}
    if 'extended_entities' in rawresult['retweeted_status'] and 'media' in rawresult['retweeted_status']["extended_entities"] :
        if rawresult['retweeted_status']["extended_entities"]['media'][0]['type']=='photo' :
            # searched_id.append(rawresult['id'])
            extractedresult['user_name']=rawresult['user']['name']
            extractedresult['user_screen_name']=rawresult['user']['screen_name']
            extractedresult['created_at'] = rawresult['created_at']
            extractedresult['retweet_count']=rawresult['retweet_count']
            extractedresult['favorite_count']=rawresult['favorite_count']
            extractedresult['media_url']=rawresult['retweeted_status']['extended_entities']['media'][0]["media_url"]
            extractedresult['tweet_url']='https://twitter.com/' + extractedresult['user_screen_name'] + '/status/' + str(rawresult['id'])
            medias = rawresult['retweeted_status']['extended_entities']['media']
            extractedresult['media_url'] = [media['media_url'] for media in medias]
            return extractedresult
        return None
    return None

    #트윗하나를 필요한정보만 추출해줌

#Notificationsearch
def extractnotification(rawresult):
    extractedresult={}
    
    if rawresult['retweeted_status']['full_text']:
        # searched_id.append(rawresult['id'])
        extractedresult['user_name']=rawresult['user']['name']
        extractedresult['user_screen_name']=rawresult['user']['screen_name']
        extractedresult['created_at'] = rawresult['created_at']
        extractedresult['Group']=rawresult['user']['name'] #이름어떻게 하지?
        extractedresult['tweet_url']='https://twitter.com/' + extractedresult['user_screen_name'] + '/status/' + str(rawresult['id'])
        simple_url_index = rawresult['retweeted_status']['full_text'].find('http')
        extractedresult['Notification']=rawresult['retweeted_status']['full_text'][:simple_url_index]
        
    return extractedresult

def get_timeline_by_id(api,user):
    timelines = tweepy.Cursor(api.user_timeline,screen_name=user, tweet_mode = 'extended').items(30)
    
    return timelines
#계정 넘겨주면 타임라인 100개 iterator로 반환해줌

#Fantweetsearch
def extractfantweetsfulltext(rawresult):
    fantweetresult={}
    
    for i in range(len(rawresult)):
        

        fantweetresult['user_name']=rawresult['user']['name']
        fantweetresult['user_screen_name']=rawresult['user']['screen_name']
        fantweetresult['created_at']=(rawresult['created_at'])
        #datetonumber
        fantweetresult['retweet_count']=rawresult['retweet_count']
        fantweetresult['favorite_count']=rawresult['favorite_count']
        fantweetresult['full_text']=rawresult['full_text'].replace(rawresult['retweeted_status']['extended_entities']['media'][0]['url'],'')
        fantweetresult['tweet_url']='https://twitter.com/' + fantweetresult['user_screen_name'] + '/status/' + str(rawresult['id'])

        return fantweetresult
    #트윗하나가 지금까지 반환한것들중에 있는지 확인해주고 아니라면 필요정보만 모아서 반환해줌

def extractfantweetswithouthastag(rawresult):
    fantweetresult={}
    
    for i in range(len(rawresult)):
        
        # if rawresult[i]['id'] in searched_id:
        #     continue
        
        # else:
        fantweetresult['user_name']=rawresult['user']['name']
        fantweetresult['user_screen_name']=rawresult['user']['screen_name']
        fantweetresult['created_at']=(rawresult['created_at'])
        #datetonumber
        fantweetresult['retweet_count']=rawresult['retweet_count']
        fantweetresult['favorite_count']=rawresult['favorite_count']
        fantweetresult['full_text']=text_without_hashtag(rawresult)
        fantweetresult['tweet_url']='https://twitter.com/' + fantweetresult['user_screen_name'] + '/status/' + str(rawresult['id'])

        return fantweetresult

def extractfantweetsonlyhastag(rawresult):
    fantweetresult={}
    
    for i in range(len(rawresult)):
        
        # if rawresult[i]['id'] in searched_id:
        #     continue
        
        # else:
        fantweetresult['user_name']=rawresult['entities']['user_mentions'][0]['name']
        fantweetresult['user_screen_name']=rawresult['entities']['user_mentions'][0]['screen_name']
        fantweetresult['created_at']=(rawresult['created_at'])
        fantweetresult['retweet_count']=rawresult['retweeted_status']['retweet_count']
        fantweetresult['favorite_count']=rawresult['retweeted_status']['favorite_count']
        fantweetresult['full_text']=rawresult['retweeted_status']['entities']['hashtags']
        fantweetresult['tweet_url']='https://twitter.com/' + fantweetresult['user_screen_name'] + '/status/' + str(rawresult['id'])

        return fantweetresult