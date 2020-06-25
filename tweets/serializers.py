# @Anyi this uses the REST API And it replaces the form.py

from rest_framework import serializers

# import model
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer)
