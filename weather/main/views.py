from django.shortcuts import render
from api.models import Temperature, Humidity, Pressure



def home(request):
    # Find the newest single temperature
    temp = Temperature.objects.order_by('-recorded_time').first()
    # Gather the total number of temperature readings gathered.
    tcount = Temperature.objects.count()
    # Find the first temperature entry recorded
    tfirst = Temperature.objects.order_by('recorded_time').first()
    humidity = Humidity.objects.order_by('-recorded_time').first()
    hcount = Humidity.objects.count()
    hfirst = Humidity.objects.order_by('recorded_time').first()
    pressure = Pressure.objects.order_by('-recorded_time').first()
    pcount = Pressure.objects.count()
    pfirst = Pressure.objects.order_by('recorded_time').first()
    
    
   
    return render(request, 'home.html', {
        'temp': temp,
         'tcount': tcount, 
         'tfirst': tfirst.recorded_time,
         'RH': humidity,
         'hcount': hcount,
         'hfirst': hfirst.recorded_time,
         'BP': pressure,
         'pcount': pcount,
         'pfirst': pfirst.recorded_time,
         
    }
    )
