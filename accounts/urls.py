from django.urls import path

from accounts.views import users
from django.conf import settings
from django.conf.urls.static import static

       
urlpatterns = [     
    path("", users.index, name="index"),   
    path("login_page",users.login_page,name="login_page") ,      
    path("signUp",users.sign_up_page,name="signUp"),
    path("authenticate_user",users.authenticate_user,name="authenticate_user"),       
    path("create_user",users.create_user,name="create_user"), 
    path("profile/<str:chartName>",users.profile,name="profile"),      
    path("login_user",users.login_user,name="login_user"),    
    path("logout_user",users.logout_user,name="logout_user"), 
    path("authentication_code",users.authentication_code,name="authentication_code"),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)