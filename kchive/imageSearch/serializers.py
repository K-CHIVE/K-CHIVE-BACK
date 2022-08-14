from rest_framework import serializers
from .models import *

class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

class NoticesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Notice
        fields = '__all__'

class FantweetsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Fantweet
        fields = '__all__'