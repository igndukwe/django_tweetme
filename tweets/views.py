from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

# @Anyi we will now use this REST Response rather than the django HttpResponse or JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication


from django.conf import settings

import random

# @Anyi import your models here
from .models import Tweet

# @Anyi import your forms here
from .forms import TweetForm

# @Anyi import your REST serializers here which can replace forms
from .serializers import TweetSerializer, TweetActionSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    # @Anyi typing http://127.0.0.1:8000/tweet/123 on the url webpage
    # args -->() kwargs -->{'tweet_id': 123}
    # >hence tweet_id declared as <int:tweet_id> from the urls.py bcoms the key here
    # >while the 123 from the http://127.0.0.1:8000/tweet/123 bcoms value
    # print(args, kwargs)
    print(request.user)
    # return HttpResponse(f"<H1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)


# @anyi this view shows the REST serialize rather than the form
@api_view(
    ["POST"]
)  # this are called decorator classess, pass list of methods you want to support,e.g. this mtd accepts a POST request
# @authentication_classes([SessionAuthentication, MyCustomAut])# users permission
@permission_classes(
    [IsAuthenticated]
)  # pass list of permisions e.g. IsAuthenticated means if users are authenticated then they have access to this form else they do not
def tweet_create_view(request, *args, **kwargs):

    # call serialiser and pass in the data
    # serializer = TweetSerializer(data=request.POST or None)#We no longer need this since the decorator ensures that
    serializer = TweetSerializer(data=request.POST)

    # raise_exception handles the try and
    if serializer.is_valid(raise_exception=True):
        # serializer.save(user=request.user, content='abc') if you want to change the content to abc
        obj = serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(["GET"])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)

    # get a single objects
    obj = qs.first()
    # pass in a single object to TweetSerializer
    serializer = TweetSerializer(obj)
    return Response(serializer.data)


@api_view(["DELETE", "POST"])  # you can use DELETE  or POST
@permission_classes([IsAuthenticated])  # checks if user can delete
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)

    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete"}, status=401)

    # get a single objects
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet removed"}, status=200)


@api_view(["POST"])  # you can use DELETE  or POST
@permission_classes([IsAuthenticated])  # is user authenticated
def tweet_action_view(request, *args, **kwargs):
    """
    id is required.
    Action options are: like, unlike, retweet
    """
    # print(request.POST, request.data)

    serializer = TweetActionSerializer(data=request.data)  # post the data here
    if serializer.is_valid(raise_exception=True):
        # @Anyi data comming in here is actually a validated data
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")

        # @Anyi filter tweet by id
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)

        # @Anyi get a single objects
        obj = qs.first()

        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
        elif action == "retweet":
            # todo
            pass

    # return Response({"message": "Tweet liked"}, status=200)
    return Response({}, status=200)


@api_view(["POST"])  # you can use DELETE  or POST
@permission_classes([IsAuthenticated])  # is user authenticated
def tweet_like_toggle_view(request, tweet_id, *args, **kwargs):
    # @Anyi filter tweet by id
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)

    # @Anyi get a single objects
    obj = qs.first()

    # @toggle
    if request.user in obj.likes.all():
        # remove it
        # @Anyi make User to unlike Tweet
        obj.likes.remove(request.user)
    else:
        # add it
        # @Anyi make User to like Tweet
        obj.likes.add(request.user)

    return Response({"message": "Tweet removed"}, status=200)


@api_view(["GET"])
def tweet_list_view(request, *args, **kwargs):
    # get a list of  query objects
    qs = Tweet.objects.all()
    # pass in many objects to TweetSerializer
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)


# @Anyi this view shows the form
def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user

    # @Anyi also go to settings.py and add LOGIN_URL = "/login"
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)

    # print("ajax", request.is_ajax())

    form = TweetForm(request.POST or None)  # Initialize the form
    # print("post data is", request.POST)
    next_url = request.POST.get("next") or None
    # print("next_url", next_url)
    if form.is_valid():
        obj = form.save(commit=False)

        # @Anyi after adding the user login
        # so the none is if user is not authenticated
        # obj.user = request.user or None  # Anonymous User will default to none
        obj.user = user

        # do ther form related logic
        obj.save()  # save values to the database
        # make sure it is ajax request
        if request.is_ajax():
            # return back to the home page
            return JsonResponse(obj.serialize(), status=201)  # 201 == created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            # return back to the home page
            return redirect(next_url)
        # else if it is not a safe url then return a form page
        form = TweetForm()  # @Anyi this resets the form

    if form.errors:
        # make sure it is ajax request
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)

    return render(request, "components/form.html", context={"form": form})


def tweet_list_view_pure_django(request, *args, **kwargs):

    """
    REST API VIEW
    Consume by JavaScript or Adjax/Swift/Java/iOs/Android
    return json data
    """

    qs = Tweet.objects.all()
    # tweets_list = [
    #    {"id": x.id, "content": x.content, "likes": random.randint(0, 129)} for x in qs
    # ]

    # @Anyi use this line of code instead of the above line
    tweets_list = [x.serialize() for x in qs]

    data = {"isUser": False, "tweet_list_response": tweets_list}
    # @Anyi this is a new way of returning our data
    # instead of HttpResponse() or render()
    # and since we want to make our page as dynamic as possible
    return JsonResponse(data)


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):

    """
    REST API VIEW
    Consume by JavaScript or Adjax/Swift/Java/iOs/Android
    return json data
    """
    data = {
        "id": tweet_id,
        # "content": obj.content,
        # "image_path": obj.image.url
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
    except:
        # If Id is not found in the url raise a 404 error
        data["message"] = "Not found"
        status = 404

    # return HttpResponse(f"<H1>Hello World {tweet_id} - {obj.content}</h1>")
    # @Anyi this is a new way of returning our data
    return JsonResponse(
        data, status=status
    )  # json.dumps content_type='application/json'

