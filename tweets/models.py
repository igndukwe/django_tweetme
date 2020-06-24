from django.db import models
from django.conf import settings

import random

# @Anyi Django has a built in User autentication
User = settings.AUTH_USER_MODEL

# Create your models here.
class Tweet(models.Model):

    # id = models.AutoField(primary_key=True) #default
    # @Anyi both content and image are not required fields
    content = models.TextField(blank=True, null=True)
    # @Anyi a path to the image is what is stored in the database
    # and not the actual image
    image = models.FileField(upload_to="images/", blank=True, null=True)

    # @Anyi to change the defult 'Tweet object(31)' to return say content
    def __str__(self):
        return self.content

    # order model in decending odder
    # so that when you refresh your html page
    # you see the most resent ones on top
    class Meta:
        ordering = ["-id"]

    def serialize(self):
        # return dictionary here
        return {"id": self.id, "content": self.content, "likes": random.randint(0, 200)}

    # @Assign Each user a foriegn key
    # one single user can own one tweet as well as many tweets
    # on the other hand one tweet can only have one user
    # CASCADE means if the owner is deleted all of the Tweets are deleted
    # SET_NULL means if the owner is deleted all of the Tweets are kept
    user = models.ForeignKey(User, on_delete=models.CASCADE)

