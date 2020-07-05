from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from .models import Tweet

# python manage.py test
user = get_user_model()
# Create your tests here.
class TweetTestCase(TestCase):
    # create as manny users as you need
    def setUp(self):
        self.user = user.objects.create_user(username="abc", password="abcd1234")
        self.userb = user.objects.create_user(username="def", password="1234abcd")
        # to create an actual Tweet in the database, it must be in the setUp
        Tweet.objects.create(content="my first tweet", user=self.user)
        Tweet.objects.create(content="my second tweet", user=self.user)
        Tweet.objects.create(content="my third tweet", user=self.userb)
        self.currentCount = Tweet.objects.all().count()

    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content="my forth tweet", user=self.user)
        self.assertEqual(tweet_obj.id, 4)
        self.assertEqual(tweet_obj.user, self.user)

    def get_client(self):
        # Make all requests in the context of a logged in session.
        client = APIClient()
        client.login(username=self.user.username, password="abcd1234")
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        # print(response.json())

    def test_tweet_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)  # one like becuse user with id 1 liked once
        # self.assertEqual(len(response.json()), 3)
        # print(response.json())

    def test_tweet_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/tweets/action/", {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)  # likes is 0 because user liked and unliked
        # self.assertEqual(len(response.json()), 3)
        # print(response.json())

    def test_tweet_retweet(self):
        client = self.get_client()
        current_count = self.currentCount
        response = client.post("/api/tweets/action/", {"id": 2, "action": "retweet"})
        #  retweet should be recreating a new tweet so its 201
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get("id")
        # make sure new tweet id is not equals the original id
        self.assertNotEqual(2, new_tweet_id)
        self.assertEqual(current_count + 1, new_tweet_id)

    def test_tweet_create_api_view(self):
        request_data = {"content": "This is my test tweet"}
        client = self.get_client()
        response = client.post("/api/tweets/create/", request_data)
        self.assertEqual(response.status_code, 201)
        request_data = response.json()
        new_tweet_id = request_data.get("id")
        self.assertEqual(self.currentCount + 1, new_tweet_id)

    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/delete")
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.get("/api/tweets/1/delete")
        self.assertEqual(response.status_code, 404)
        response_incorect_ownrer = client.get("/api/tweets/3/delete")
        self.assertEqual(response_incorect_ownrer.status_code, 401)
