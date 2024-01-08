from django.urls import path

from accounts.views import users,home
from django.conf import settings
from django.conf.urls.static import static

       
urlpatterns = [     
    path("", users.index, name="index"),   
    path("login_page",users.login_page,name="login_page") ,      
    path("signUp",users.sign_up_page,name="signUp"),
    path("authenticate_user",users.authenticate_user,name="authenticate_user"),       
    path("create_user",users.create_user,name="create_user"), 
    path("profile/<str:chart_name>",users.profile,name="profile"),      
    path("login_user",users.login_user,name="login_user"),    
    path("logout_user",users.logout_user,name="logout_user"), 
    path("authentication_code",users.authentication_code,name="authentication_code"),
    path("search_users/<str:input_text>",users.search_users,name="search_users"),
    path("other_user_profile/<str:username>/<str:chart_name>",users.other_user_profile,name="other_user_profile"), 
    path('home',home.home,name='home'),  
    path("send_friend_requeast/<str:username>",users.send_friend_requeast,name="send_friend_requeast")  ,
    path("get_friendship_status/<str:username>",users.get_friendship_status,name="get_friendship_status"),
    path("friend_request_handler/<str:username>",users.friend_request_handler,name="friend_request_handler"),
    path("unread_notification",users.unread_friend_request,name="unread_notification") ,
    path('friend_request_page',users.friend_request_page,name='friend_request_page')        
    ]     
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)