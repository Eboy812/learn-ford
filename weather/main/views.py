from django.shortcuts import render
from api.models import Temperature, Humidity, Pressure
from django.db.models import Max, Min, F
from datetime import datetime, timedelta
from chartjs.views.lines import BaseLineChartView

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class LineChartView(BaseLineChartView):
    type = ''
    labels = []
    max_list = []
    min_list = []
    
    def set_minmax(self, index, item):
        
        if self.type == 'temp':
            item = c2f(item)
    
        if item > self.max_list[index]:
            self.max_list[index] = (item)
            
        if item < self.min_list[index]:
            self.min_list[index] = (item)
    
    def last_seven_days(self):
        self.type = self.kwargs.get('type')
        now = datetime.now()
        seven_days_ago = now - timedelta(days = 7)
        
        if self.type == 'RH':
            datas = Humidity.objects.order_by('-recorded_time').filter(recorded_time__range=(seven_days_ago,now)).annotate(value=F('rh'))
        elif self.type == 'BH':
            datas = Pressure.objects.order_by('-recorded_time').filter(recorded_time__range=(seven_days_ago,now)).annotate(value=F('pressure'))
        else:
            datas = Temperature.objects.order_by('-recorded_time').filter(recorded_time__range=(seven_days_ago,now)).annotate(value=F('celsius'))
        
        print(datas)
    
        for data in datas:
            weekday = datetime.weekday(data.recorded_time)
            print(str(data.recorded_time) +' = '+ str(weekday) +' '+ days[weekday])
            if days[weekday] not in self.labels:
                self.labels.append(days[weekday])
                
        self.max_list = [-100 for i in range(len(self.labels))]
        self.min_list = [9999 for i in range(len(self.labels))]
        
        for data in datas:
            weekday = datetime.weekday(data.recorded_time)
            idx = self.labels.index(days[weekday])
            self.set_minmax(idx, data.value)

    
    def get_providers(self):
        """ Return the names for the data sets. """
        return['Max', 'Min']
        
    def get_labels(self):
        # Return labels for our days
        return self.labels
        
    def get_data(self):
        # returns min, max data sets to draw
        
        self.last_seven_days()
        
        return [self.max_list, self.min_list]


def c2f(celsius):
    return((celsius * 9/5) + 32)


def home(request):
    now = datetime.now()
    sometime_ago = now - timedelta(days = 7)
    temp_max = c2f(Temperature.objects.filter(recorded_time__range=(sometime_ago,now)).aggregate(Max('celsius'))['celsius__max'])
    temp_min = c2f(Temperature.objects.filter(recorded_time__range=(sometime_ago,now)).aggregate(Min('celsius'))['celsius__min'])
    RH_max = (Humidity.objects.filter(recorded_time__range=(sometime_ago,now)).aggregate(Max('rh'))['rh__max'])
    RH_min = (Humidity.objects.filter(recorded_time__range=(sometime_ago,now)).aggregate(Min('rh'))['rh__min'])
    BP_max = (Pressure.objects.filter(recorded_time__range=(sometime_ago,now)).aggregate(Max('pressure'))['pressure__max'])
    BP_min = (Pressure.objects.filter(recorded_time__range=(sometime_ago,now)).aggregate(Min('pressure'))['pressure__min'])
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
