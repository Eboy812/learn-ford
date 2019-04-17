from rest_framework import serializers
from . import models



class TemperatureSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'celsius', 'change', 'recorded_time')
        model = models.Temperature
        
class HumiditySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'rh', 'change', 'recorded_time')
        model = models.Humidity
        
class PressureSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'pressure', 'change', 'recorded_time')
        model = models.Pressure