from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Tweet

# Create your views here.
def home_view(request, *args, **kwargs):
    # @Anyi typing http://127.0.0.1:8000/tweet/123 on the url webpage
    # args -->() kwargs -->{'tweet_id': 123}
    # >hence tweet_id declared as <int:tweet_id> from the urls.py bcoms the key here
    # >while the 123 from the http://127.0.0.1:8000/tweet/123 bcoms value
    print(args, kwargs)
    # return HttpResponse(f"<H1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)


def tweet_list_view(request, *args, **kwargs):

    """
    REST API VIEW
    Consume by JavaScript or Adjax/Swift/Java/iOs/Android
    return json data
    """

    qs = Tweet.objects.all()
    tweets_list = [{"id": x.id, "content": x.content} for x in qs]

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

