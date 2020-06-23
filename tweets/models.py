from django.db import models
import random

# Create your models here.
class Tweet(models.Model):
    # id = models.AutoField(primary_key=True) #default
    # @Anyi both content and image are not required fields
    content = models.TextField(blank=True, null=True)
    # @Anyi a path to the image is what is stored in the database
    # and not the actual image
    image = models.FileField(upload_to="images/", blank=True, null=True)

    # order model in decending odder
    # so that when you refresh your html page
    # you see the most resent ones on top
    class Meta:
        ordering = ["-id"]

    def serialize(self):
        # return dictionary here
        return {"id": self.id, "content": self.content, "likes": random.randint(0, 200)}
