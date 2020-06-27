"""tweetme2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from tweets.views import (
    home_view,
    tweet_detail_view,
    tweet_action_view,
    tweet_delete_view,
    tweet_list_view,
    tweet_create_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # @Anyi http://127.0.0.1:8000
    path("", home_view, name="home_view"),
    #####Dynamic URL#######
    # @Anyi http://127.0.0.1:8000/tweets/1
    # path("tweets/<int:tweet_id>", home_view, name="home_view"),
    path("tweets/<int:tweet_id>", tweet_detail_view, name="tweet_detail_view"),
    # @Anyi http://127.0.0.1:8000/tweets
    path("tweets", tweet_list_view, name="tweet_list_view"),
    # @Anyi http://127.0.0.1:8000/create-tweet
    path("create-tweet", tweet_create_view, name="tweet_create_view"),
    # @Anyi http://127.0.0.1:8000/api/tweets/1/delete
    # api means that we are appending the REST API
    path(
        "api/tweets/<int:tweet_id>/delete", tweet_delete_view, name="tweet_delete_view"
    ),
    # @Anyi http://127.0.0.1:8000/api/tweets/action
    path("api/tweets/action", tweet_action_view, name="tweet_action_view"),
]
