from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.models import AbstractUser

#class User(models.Model):
#    userID = models.AutoField(primary_key=True)
#    email = models.EmailField(unique=True)
#    password = models.CharField(max_length=128)
#    userName = models.CharField(max_length=50)

#    def set_password(self, raw_password):
#        self.password = make_password(raw_password)

#    def check_password(self, raw_password):
#        return check_password(raw_password, self.password)

#    def __str__(self):
#        return self.userName

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.userName


class ImageModel(models.Model):
    imageID = models.AutoField(primary_key=True)
    image_base64 = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"Image {self.imageID} - {self.image_base64}"

class UsageHistory(models.Model):
    operationID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    imageID = models.ForeignKey(ImageModel, on_delete=models.SET_NULL, null=True)
    prompt = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Operation {self.operationID} - User {self.userID} - Image {self.imageID}"
