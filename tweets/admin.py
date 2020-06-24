from django.contrib import admin

from .models import Tweet


# improve the search in the admin page in terms of content and user
class TweetAdmin(admin.ModelAdmin):

    list_display = [
        "__str__",
        "user",
    ]  # @Anyi displays the user field as a column in the tweet
    search_fields = ["content", "user__username", "user__email"]

    class Meta:
        model = Tweet


# Register your models here.
admin.site.register(Tweet, TweetAdmin)

