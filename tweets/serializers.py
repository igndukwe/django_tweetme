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
