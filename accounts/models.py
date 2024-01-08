from django.db import models
from django.contrib.auth.models import User

from django.db.models.functions import Coalesce


class FriendsRequestModel(models.Model):
    date= models.DateTimeField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    accepted=models.BooleanField(default=False) 
    request_seen=models.BooleanField(default=False)  
    accepted_seen= models.BooleanField(default=False) 

