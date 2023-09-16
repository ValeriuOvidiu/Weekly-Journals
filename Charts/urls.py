from django.urls import path

from Charts.views import users_views, charts_views,jurnals_views
from django.conf import settings
from django.conf.urls.static import static

       
urlpatterns = [     
    path("", users_views.index, name="index"),   
    path("login_page",users_views.login_page,name="login_page") ,      
    path("signUp",users_views.signUp,name="signUp"),
    path("authenticate_user",users_views.authenticate_user,name="authenticate_user"),       
    path("create_user",users_views.create_user,name="create_user"), 
    path("profile/<str:chartName>",users_views.profile,name="profile"),      
    path("login_user",users_views.login_user,name="login_user"),    
    path("logout_user",users_views.logout_user,name="logout_user"), 
    path("authentication_code",users_views.authentication_code,name="authentication_code"),
    path('get_data_for_work_chart/<str:username>/<str:searched_date>', charts_views.WorkedChartData.as_view(), name='get_data'),
    path("worked_hours_save",charts_views.worked_hours_save,name="worked_hours_save"),    
    path("search_by_date/<str:chartName>", charts_views.search_by_date ,name="search_by_date"),  
    path('get_data_for_sleep_chart/<str:username>/<str:searched_date>', charts_views.SleptChartData.as_view(), name='get_data_for_sleep_chart'),
    path("slept_hours_save",charts_views.slept_hours_save,name="slept_hours_save"), 
    path("jurnals_data/<str:username>/<str:searched_date>",charts_views.JurnalsChartData.as_view(),name="jurnals_data"), 
    path("upload_jurnal",jurnals_views.upload_jurnal,name="upload_jurnal"),
    path("upload_calendar_image",jurnals_views.upload_calendar_image,name="upload_calendar_image"),
    path("edit",jurnals_views.edit_jurnal,name="edit")  

     
]        

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
