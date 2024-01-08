import os
from django.core.asgi import get_asgi_application
from django.urls import re_path
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from channels.auth import AuthMiddlewareStack
from django.urls import path
from channels.routing import ProtocolTypeRouter,URLRouter
from accounts import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weekly_journals.settings')
django_asgi_app = get_asgi_application()    
application=ProtocolTypeRouter({  
    "http": django_asgi_app,
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(       
            URLRouter(
                [       
                    path("ws/<str:id>",consumers.FriendRequestConsumer.as_asgi(),name="ws"),    
            
                ]   
            )
        )
    )

})    