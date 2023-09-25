from django.urls import path

from  charts.views import  charts_data,journals
from django.conf import settings   
from django.conf.urls.static import static

       
urlpatterns = [     
    path('get_data_for_work_chart/<str:username>/<str:searched_date>', charts_data.WorkedChartData.as_view(), name='get_data'),
    path("worked_hours_save",charts_data.worked_hours_save,name="worked_hours_save"),    
    path("search_by_date/<str:chartName>", charts_data.search_by_date ,name="search_by_date"),  
    path('get_data_for_sleep_chart/<str:username>/<str:searched_date>', charts_data.SleptChartData.as_view(), name='get_data_for_sleep_chart'),
    path("slept_hours_save",charts_data.slept_hours_save,name="slept_hours_save"), 
    path("journals_data/<str:username>/<str:searched_date>",charts_data.JournalsChartData.as_view(),name="jurnals_data"), 
    path("upload_journal",journals.upload_journal,name="upload_jurnal"),
    path("upload_calendar_image",journals.upload_calendar_image,name="upload_calendar_image"),
    path("edit",journals.edit_journal,name="edit"),     
]        

if settings.DEBUG:   
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
