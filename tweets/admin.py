from django.contrib import admin

# Register your models here.
from .models import Tweet, TweetLike

# @Anyi set the TweetLike ready to be customized in the Admin as a Table
class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike


# @Anyi set the Tweet ready to be customized in the Admin as a Detail
# we can improve the search in the admin page in terms of content and user
class TweetAdmin(admin.ModelAdmin):
    inlines = [TweetLikeAdmin]
    # @Anyi display user list associated to each tweet on this page
    list_display = ["__str__", "user"]

    # @Anyi displays the user field as a columns on the Tweet page
    search_fields = ["content", "user__username", "user__email"]

    class Meta:
        model = Tweet


# Register your models here.
admin.site.register(Tweet, TweetAdmin)
