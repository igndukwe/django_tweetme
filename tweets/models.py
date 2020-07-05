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

    #####    ONE TO MANY    #######
    # Only One User Can Own A Tweet
    # @Anyi assign each user a foriegn key
    # one single user can own one tweet as well as many tweets
    # on the other hand one tweet can only have one user
    # >CASCADE means if the owner is deleted all of the Tweets are deleted
    # >SET_NULL means if the owner is deleted all of the Tweets are kept
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    ######    SELF REFERENCE    ############
    # @Anyi The idea of Tweet having a FK that references its self
    # This is the idea that a user can retweet itself,
    # in some cases they can have comments there
    # > use "self" to seference the same model
    # models.SET_NULL means when this field is deleted do not delete its references rather set to null
    # Hence by default a Tweet will never have a parent except it is retweeted
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)

    #####    MANY TO MANY    #######
    # Many Users Can like A Tweet
    # @Anyi create a likes field with a Many to Many relationship
    # i.e. One tweet can have Many users and Many users can have One tweet
    # This allows to add individual users to the likes
    # >It is similar to ForeignKey,
    # but the difference is that I can have a list of users here Vs. One User in the FK
    # > through=TweetLike creates an instance of the timestamp
    # we do not hae to add the through=TweetLike
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

    @property
    def is_retweet(self):
        # if parent is equals to none then it is a not a retweet otherwise, it is a retweet
        return self.parent != None

    # return dictionary here in a serialized format (this is the old way)
    def serialize(self):
        return {"id": self.id, "content": self.content, "likes": random.randint(0, 200)}


#####   TweetLike   ####
# @Anyi How to access this model
# e.g.
# @Anyi get all the tweet likes
# TweetLike.objects.all()
# @Anyi delete all the tweet likes
# TweetLike.objects.all().delete()

#####   Tweet   ####
# @Anyi call the first tweet
# obj = Tweet.objects.first()
# access all the likes by that tweet (becos its many to many field)
# obj.likes.all()

#####   User   ####
# @Anyi we can also import the default User model
# from django.contrib.auth import get_user_model
# instantiate the user model
# user = get_user_model()
# Get all the users
# user.objects.all()
# Get the first user
# me = user.objects.first()
# me

# 1
# @Anyi we can now make the me user to like a tweet
# obj.likes.add(me)
# see the uses that have liked a tweet
# obj.likes.all()
# to unlike
# obj.likes.remove(me)
# see that the user is gone
# obj.likes.all()

# @Anyi notice that all users can also like a tweet (Many to Many)
# get all the users
# qs = user.objects.all()
# get all users to like a tweet
# obj.likes.set(qs)
# see that all the users have liked the tweet
# obj.likes.all()

# @Anyi we can also see the timestamp a tweet was liked
# e.g. lets see the timestamp the first tweet was liked
# TweetLike.objects.first().timestamp

# lets delete all tweets associated with the me user
# obj.likes.remove(me)
# check to see, since its only one user for now
# obj.likes.all()


# 2.
# @Anyi another way to make a user like a tweet
# TweetLike.objects.create(user=me, tweet=obj)
# check
# obj.likes.all()

# 3.
# @Anyi you can also add an empty set (this deletes a group of user likes/ or provides a way to filter)
# empty_users = user.objects.none()
# empty_users
# empty the likes
# obj.likes.set(empty_users)
# obj.likes.all()

