###########################################################
# @Anyi this uses the REST API
# The serializer.py replaces the form.py                  #
###########################################################
# @Anyi settings.py is in the django configuration file
from django.conf import settings
from rest_framework import serializers

# import model class
from .models import Tweet

# Declared MAX_TWEET_LENGTH and TWEET_ACTION_OPTIONS
# in the settings.py as a global variable and I am invoking theme here
MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

# @Anyi make a serialiser for Tweets Actions
# using just Serializer not ModelSerializer
# because Tweets Action gets information directly from the view
# the main purpose of this serialiser is to validate the input coming from the form
class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()  # required field
    action = serializers.CharField()  # required field
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valied action for tweets")
        return value


# @Anyi make a serialiser for Tweets
class TweetCreateSerializer(serializers.ModelSerializer):

    ####    LABELS   ####
    # what you want the fields to be like
    likes = serializers.SerializerMethodField(read_only=True)

    ####    DEFINE FIELDS AND METHODS YOU ARE SERIALIZING  ####
    class Meta:
        model = Tweet
        fields = ["id", "content", "likes"]  # i want to change likes to numbers

    # @Anyi this counts the number of likes
    def get_likes(self, obj):
        return obj.likes.count()

    # @Anyi this method is similar to the form, however use validate__fieldname rather than clean_fieldname
    # @Anyi enter validate and the name the field you want to calidate
    def validate_content(self, content):
        # @Anyi we moved remember we moved MAX_TWEET_LENGTH=240 to settings.py
        if len(content) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return content


# @Anyi make a serialiser for Tweets
class TweetSerializer(serializers.ModelSerializer):

    ####    LABELS   ####
    # what you want the fields to be like
    # e.g. like and content fields should be read only
    # remember that by default you can not change the if field
    # > i.e. add in a serialized version of the parent object
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)
    # you can also renam what this label will be in
    # original_tweet = TweetCreateSerializer(source="parent", read_only=True)
    # content = serializers.SerializerMethodField(read_only=True)
    # is_retweet  #re-tweet is a mtd and I do not have to call it

    ####    DEFINE FIELDS AND METHODS YOU ARE SERIALIZING  ####
    class Meta:
        model = Tweet
        # fields = ["id", "content", "likes", "is_retweet", "original_tweet"]
        fields = ["id", "content", "likes", "is_retweet", "parent"]

    ####    USE THE FIELDS   ####
    # @Anyi this counts the number of likes
    # i want to change likes to numbers
    def get_likes(self, obj):
        return obj.likes.count()

    # def get_content(self, obj):
    #    content = obj.content
    #    if obj.is_retweet:
    #        content = obj.parent.content
    #    return content

