from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True, null=True)
  address = models.CharField(max_length=64, null=True)
  rating = models.FloatField(null=True) #NEEDS TO HAVE NULL=True
  num_of_ratings = models.IntegerField(null=True)

class Userrating (models.Model):
  rating = models.IntegerField()
  sender = models.ForeignKey(UserProfile, related_name='Userrating_sender')
  receiver = models.ForeignKey(UserProfile, related_name='Userrating_receiver')