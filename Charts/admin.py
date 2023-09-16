from django.contrib import admin
from Charts.models import HoursWorkedModel,HoursSleptModel,WeeklyJurnalModel,CalendarImageModel,Choices

# Register your models here.
admin. site. register(HoursWorkedModel)      
admin. site. register(HoursSleptModel)
admin. site. register(WeeklyJurnalModel)
admin. site. register(CalendarImageModel)  
admin. site. register(Choices)
   