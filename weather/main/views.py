from django.shortcuts import render
from api.models import Temperature, Humidity, Pressure
from django.db.models import Max, Min
from datetime import datetime, timedelta


def c2f(celsius):
    return((celsius * 9/5) + 32)


def home(request):
    now = datetime.now()
    sometime_ago = now - timedelta(days = 7)
    temp_max = c2f(Temperature.objects.filter(recorded_time__range=(sometime_ago,now)).aggregate(Max('celsius'))['celsius__max'])
    temp_min = c2f(Temperature.objects.filter(recorded_time__range=(sometime_ago,now)).aggregate(Min('celsius'))['celsius__min'])
    RH_max = c2f(Humidity.objects.filter(recorded_time__range=(sometime_ago,now)).aggregate(Max('rh'))['rh__max'])
    RH_min = c2f(Humidity.objects.filter(recorded_time__range=(sometime_ago,now)).aggregate(Min('rh'))['rh__min'])
    BP_max = c2f(Pressure.objects.filter(recorded_time__range=(sometime_ago,now)).aggregate(Max('pressure'))['pressure__max'])
    BP_min = c2f(Pressure.objects.filter(recorded_time__range=(sometime_ago,now)).aggregate(Min('pressure'))['pressure__min'])
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
         'result_count': tcount + hcount + pcount,
         'temp_max': temp_max,
         'temp_min': temp_min,
         'RH_max':RH_max,
         'RH_min':RH_min,
         'BP_max':BP_max,
         'BP_min':BP_min
         
    }
    )
