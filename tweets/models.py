import random
from django.conf import settings
from django.db import models

# @Anyi Django has a built in User autentication
User = settings.AUTH_USER_MODEL

# Create your models here.


class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # @Anyi use quotes for the "Tweet" becos the Tweet model class is below the TweetLike model class
    # i.e becos the Tweet model class is referenced before it is declared
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    # @Anyi we want to measure the time a tweet was liked
    timestamp = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
    # Maps to SQL data
    # @Anyi id is there by default
    # id = models.AutoField(primary_key=True)

    #####Only One User Can Own A Tweet#####
    # @Anyi assign each user a foriegn key
    # one single user can own one tweet as well as many tweets
    # on the other hand one tweet can only have one user
    # >CASCADE means if the owner is deleted all of the Tweets are deleted
    # >SET_NULL means if the owner is deleted all of the Tweets are kept
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #####Many Users Can like A Tweet#####
    # @Anyi create a likes field with a Many to Many relationship
    # i.e. One tweet can have Many users and Many users can have One tweet
    # This allows to add individual users to the likes
    # >It is similar to ForeignKey,
    # but the difference is that I can have a list of users here Vs. One User in the FK
    # > we do not hae to add the through=TweetLike
    # all it does is that it adds a timestamp a tweet was liked
    # to the many to many reference
    # this will be good to keeptrack of what users liked over time
    likes = models.ManyToManyField(
        User, related_name="tweet_user", blank=True, through=TweetLike
    )

    #####Other Fields#######
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to="images/", blank=True, null=True)
    # timestamp for the tweet itself
    timestamp = models.DateTimeField(auto_now_add=True)

    # @Anyi this changes the defult object field:'Tweet object(31)' to return say the content field`
    # def __str__(self):
    #     return self.content

    # @Anyi we want the model to be in displayed in decending order
    # when you refresh your html page su that we can see the most recent tweets on top
    class Meta:
        ordering = ["-id"]

    # return dictionary here in a serialized format (this is the old way)
    def serialize(self):
        return {"id": self.id, "content": self.content, "likes": random.randint(0, 200)}

