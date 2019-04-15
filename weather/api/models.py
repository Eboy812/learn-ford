from django.db import models

# Create your models here.


class Temperature(models.Model):
    celsius = models.FloatField(default=0.0)
    change = models.FloatField(default=0.0)
    recorded_time = models.DateTimeField(auto_now=True)
    
    @property
    def fahrenheit(self):
        "Returns the temperature in fahrenheit"
        return '%f' % ((self.celsius * 9/5) +32)

    
    def __str__(self):
        return str(self.celsius)
        
class Pressure(models.Model):
    pressure = models.FloatField(default=0.0)
    change = models.FloatField(default=0.0)
    recorded_time = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return str(self.pressure)


class Humidity(models.Model):
    pass


