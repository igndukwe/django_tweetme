from django.urls import path

from .views import (
    home_view,
    tweet_action_view,
    tweet_delete_view,
    tweet_detail_view,
    tweet_list_view,
    tweet_create_view,
)

"""
CLIENT
Base ENDPOINT /api/tweets/
"""
urlpatterns = [
    # @Anyi http://127.0.0.1:8000/tweets/
    path("", tweet_list_view),
    # @Anyi http://127.0.0.1:8000/tweets/action/
    path("action/", tweet_action_view),
    # @Anyi http://127.0.0.1:8000/tweets/1/
    path("create/", tweet_create_view),
    # @Anyi http://127.0.0.1:8000/create/
    path("<int:tweet_id>/", tweet_detail_view),
    # @Anyi http://127.0.0.1:8000/tweets/1/delete/
    path("<int:tweet_id>/delete/", tweet_delete_view),
]
