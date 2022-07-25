from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Ads,AdsImages,User,Author
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        # fields = '__all__'
        #  class Meta:
       
        fields='__all__'


class AdsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsImages
        # fields = '__all__'
        #  class Meta:
       
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        #  class Meta:
       
        fields='__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        # fields = '__all__'
        #  class Meta:
       
        fields='__all__'