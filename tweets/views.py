from django.http import HttpResponse, Http404
from django.shortcuts import render

from .models import Tweet

# Create your views here.
def home_view(request, *args, **kwargs):
    # @Anyi typing http://127.0.0.1:8000/tweet/123 on the url webpage
    # args -->() kwargs -->{'tweet_id': 123}
    # >hence tweet_id declared as <int:tweet_id> from the urls.py bcoms the key here
    # >while the 123 from the http://127.0.0.1:8000/tweet/123 bcoms value
    print(args, kwargs)
    return HttpResponse(f"<H1>Hello World</h1>")


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    # print("tweet_id:", tweet_id)
    try:
        obj = Tweet.objects.get(id=tweet_id)
    except:
        # If Id is not found in the url raise a 404 error
        raise Http404
    return HttpResponse(f"<H1>Hello World {tweet_id} - {obj.content}</h1>")
