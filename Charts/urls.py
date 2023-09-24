from django.urls import path

from Charts.views import  charts,journals
from django.conf import settings   
from django.conf.urls.static import static

       
urlpatterns = [     
    path('get_data_for_work_chart/<str:username>/<str:searched_date>', charts.WorkedChartData.as_view(), name='get_data'),
    path("worked_hours_save",charts.worked_hours_save,name="worked_hours_save"),    
    path("search_by_date/<str:chartName>", charts.search_by_date ,name="search_by_date"),  
    path('get_data_for_sleep_chart/<str:username>/<str:searched_date>', charts.SleptChartData.as_view(), name='get_data_for_sleep_chart'),
    path("slept_hours_save",charts.slept_hours_save,name="slept_hours_save"), 
    path("journals_data/<str:username>/<str:searched_date>",charts.JournalsChartData.as_view(),name="jurnals_data"), 
    path("upload_journal",journals.upload_journal,name="upload_jurnal"),
    path("upload_calendar_image",journals.upload_calendar_image,name="upload_calendar_image"),
    path("edit",journals.edit_journal,name="edit"),     
]        

if settings.DEBUG:   
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
