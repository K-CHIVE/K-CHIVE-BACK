from rest_framework.views import APIView
from django.conf import settings
import tweepy
from common.views import connect_api, get_tweet_by_keyword
from django.http import HttpResponse
from pprint import pprint

class Posting:
    def __init__(self, id, created_at, hashtags, full_text, tweet_url, retweet_count,  favorite_count, user_screen_name, user_name, user_profile_image_url, media_url):
        self.id = id
        self.created_at = created_at
        self.hashtags = hashtags
        self.full_text = full_text
        self.tweet_url = tweet_url
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count
        self.user_screen_name = user_screen_name
        self.user_name = user_name
        self.user_profile_image_url = user_profile_image_url
        self.media_url = media_url


class GoodsListView(APIView):
    def get(self, request):
        api = connect_api()
        group = request.GET.get('group', '')
        member = request.GET.get('member', '')
        keyword = group + member + "굿즈"
        print(keyword)
        result = []
        tweets = get_tweet_by_keyword(api, keyword)
        for index, status in enumerate(tweets):
            status = status._json
            # print(status["entities"]["media"][0]["media_url"])
            # break
            # print(status)
            # print(status["entities"]["urls"]["url"])

            # print(status["retweeted_status"]
            #       ["entities"]["media"][0]["media_url"] if hasattr(status, "retweeted_status") else [])
            # print(status["entities"]["media"]
            #       if hasattr(status, "entities") else [])
            # print(status["entities"]["media"][0]["media_url"])
            if 'retweeted_status' in status : 
                if index >= 100:
                    break
                if 'extended_entities' in status['retweeted_status'] :
                    medias = status['retweeted_status']['extended_entities']['media']
                    media_urls = [media['media_url'] for media in medias]
                else :
                    media_urls = []
                tweet_url = 'https://twitter.com/' + status['entities']['user_mentions'][0]['screen_name'] + '/status/' + str(status['id'])
                posting = Posting(status["id_str"], status["created_at"], status.entities.hashtag if hasattr(status, 'entities.hashtag') else [], status["full_text"], tweet_url, status["retweet_count"],
                                status["favorite_count"], status["user"]["screen_name"], status["user"]["name"], status["user"]["profile_image_url"], media_urls)
                result.append(vars(posting))

        print("검색 성공")
        # print(result)

        return HttpResponse(result, status=200)
