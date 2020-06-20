from django.db import models

# Create your models here.
class Tweet(models.Model):
    # id = models.AutoField(primary_key=True) #default
    # @Anyi both content and image are not required fields
    content = models.TextField(blank=True, null=True)
    # @Anyi a path to the image is what is stored in the database
    # and not the actual image
    image = models.FileField(upload_to="images/", blank=True, null=True)
