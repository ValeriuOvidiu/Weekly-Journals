from django.contrib import admin
from charts.models import HoursWorkedModel,HoursSleptModel,WeeklyJournalModel,CalendarImageModel,Choices

# Register your models here.
admin. site. register(HoursWorkedModel)      
admin. site. register(HoursSleptModel)
admin. site. register(WeeklyJournalModel)
admin. site. register(CalendarImageModel)  
admin. site. register(Choices)
   