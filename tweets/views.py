from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from django.conf import settings

import random

# @Anyi import your models here
from .models import Tweet

# @Anyi import your forms here
from .forms import TweetForm

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


# @Anyi this view shows the form
def tweet_create_view(request, *args, **kwargs):
    # print("ajax", request.is_ajax())

    form = TweetForm(request.POST or None)  # Initialize the form
    # print("post data is", request.POST)
    next_url = request.POST.get("next") or None
    # print("next_url", next_url)
    if form.is_valid():
        obj = form.save(commit=False)
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


def tweet_list_view(request, *args, **kwargs):

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


def tweet_detail_view(request, tweet_id, *args, **kwargs):

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

