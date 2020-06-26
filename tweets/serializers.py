###########################################################
# @Anyi this uses the REST API
# The serializer.py replaces the form.py                  #
###########################################################
# @Anyi settings.py is in the django configuration file
from django.conf import settings
from rest_framework import serializers

# import model class
from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

# @Anyi make a serialiser for Tweets Actions
# using just Serializer not ModelSerializer because Tweets Action not a model
class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()  # required field
    action = serializers.CharField()  # required field

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valied action for tweets")
        return value


# @Anyi make a serialiser for Tweets
class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ["content"]

    # @Anyi this method is similar to the form, however use validate__fieldname rather than clean_fieldname
    # @Anyi enter validate and the name the field you want to calidate
    def validate_content(self, content):
        # @Anyi we moved remember we moved MAX_TWEET_LENGTH=240 to settings.py
        if len(content) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return content
