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

def text_without_hashtag(rawresult):
    fulltext=rawresult['retweeted_status']['full_text']
    hashtags=rawresult['retweeted_status']['entities']['hashtags']
    textwithouthashtag=fulltext
    for i in range(len(hashtags)):
        textwithouthashtag=textwithouthashtag.replace('#'+hashtags[i]['text'],'')
    return textwithouthashtag
#원본 트윗을 넘겨주면 해시태그 없는 본문을 반환함

def filter_by_daterange(startdate,enddate,objectdict):
    time=objectdict['created_at']
    if objectdict>=int(startdate) and objectdict<=int(enddate):
        return objectdict
    else:
        return None

#날짜범위와 트윗하나를 넘겨주면 범위에 맞는지 체크해서 걸러줌
def filtered_by_daterange(startdate,enddate,objects):
    resultsfilteredbydaterange=[]
    for i in range(len(objects)):
        resultsfilteredbydaterange.append(filter_by_daterange(startdate,enddate,objects[i]))
    return resultsfilteredbydaterange



def get_timeline_by_id(api,user):
    timelines = tweepy.Cursor(api.user_timeline, id = user).items(100)
    return timelines
#계정 넘겨주면 타임라인 100개 iterator로 반환해줌

def datetonumber(date):
    Dow,Month,Date,Time,Nation,Year=date.split()
    MonthEng=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    MonthEngDict={}
    for i,v in enumerate(MonthEng):
        MonthEngDict[v]='%02d'%(i+1)
    EngMonthinNum=MonthEngDict[Month]
    DateintoNumber=Year[-1]+Year[-2]+EngMonthinNum+Date
    return DateintoNumber
        
    


searched_id=[]


def extract(rawresults):
    if 'extended_entities' in rawresults:
        searched_id.append(rawresults['id'])
        extractedresults={}
        extractedresults['user_name']=rawresults['entities']['user_mentions'][0]['name']
        extractedresults['user_screen_name']=rawresults['entities']['user_mentions'][0]['screen_name']
        extractedresults['created_at']=datetonumber(rawresults['created_at'])
        extractedresults['retweet_count']=rawresults['retweeted_status']['retweet_count']
        extractedresults['in_reply_to_status_id']=rawresults['in_reply_to_status_id']
        extractedresults['favorite_count']=rawresults['retweeted_status']['favorite_count']
        extractedresults['media_url']=rawresults['retweeted_status']['extended_entities']['media']
        extractedresults['tweet_url']=rawresults['full_text'][rawresults['full_text'].find('http'):]
        return extractedresults
    else:
        return None#맞나

    #gif는 나중에 추가 file 로 되어있는지 media로 되어있는지 확인
    #사진을 누르면 해당 트윗으로 이동하게 url추가해야하나? yes

def extractnotification(rawresults):
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
            fantweetresult['created_at']=datetonumber(rawresults['created_at'])
            fantweetresult['retweet_count']=rawresults['retweeted_status']['retweet_count']
            fantweetresult['in_reply_to_status_id']=rawresults['in_reply_to_status_id']
            fantweetresult['favorite_count']=rawresults['retweeted_status']['favorite_count']
            fantweetresult['full_text']=rawresults['retweeted_status']['full_text']

            return fantweetresult

def extractfantweetswithouthastag(rawresults):
    for i in range(len(rawresults)):
        if rawresults[i]['id'] in searched_id:
            continue
        else:
            fantweetresult={}
            fantweetresult['user_name']=rawresults['entities']['user_mentions'][0]['name']
            fantweetresult['user_screen_name']=rawresults['entities']['user_mentions'][0]['screen_name']
            fantweetresult['created_at']=datetonumber(rawresults['created_at'])
            fantweetresult['retweet_count']=rawresults['retweeted_status']['retweet_count']
            fantweetresult['in_reply_to_status_id']=rawresults['in_reply_to_status_id']
            fantweetresult['favorite_count']=rawresults['retweeted_status']['favorite_count']
            fantweetresult['full_text']=text_without_hashtag(rawresults)

            return fantweetresult

def extractfantweetsonlyhastag(rawresults):
    for i in range(len(rawresults)):
        if rawresults[i]['id'] in searched_id:
            continue
        else:
            fantweetresult={}
            fantweetresult['user_name']=rawresults['entities']['user_mentions'][0]['name']
            fantweetresult['user_screen_name']=rawresults['entities']['user_mentions'][0]['screen_name']
            fantweetresult['created_at']=datetonumber(rawresults['created_at'])
            fantweetresult['retweet_count']=rawresults['retweeted_status']['retweet_count']
            fantweetresult['in_reply_to_status_id']=rawresults['in_reply_to_status_id']
            fantweetresult['favorite_count']=rawresults['retweeted_status']['favorite_count']
            fantweetresult['full_text']=rawresults['retweeted_status']['entities']['hashtags']

            return fantweetresult