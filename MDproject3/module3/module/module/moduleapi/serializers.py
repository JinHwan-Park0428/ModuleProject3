from module.moduleapi.models import MyProjectStock, MyProjectWeather
from rest_framework import serializers

class MyProjectStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyProjectStock
        fields = ['quantity', 'price', 'days_range', 'title','open_price','ratio','search_time']

class MyProjectWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyProjectWeather
        fields = ['temper','humid','high_temp','low_temp','title','wind','weather','search_time']