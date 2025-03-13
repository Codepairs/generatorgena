from django.db import models

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    userName = models.CharField(max_length=50)

    def __str__(self):
        return self.userName

class Image(models.Model):
    imageID = models.AutoField(primary_key=True)
    link_to_image = models.URLField()
    createdAt = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"Image {self.imageID} - {self.link_to_image}"

class Usage_history(models.Model):
    operationID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    imageID = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    prompt = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Operation {self.operationID} - User {self.userID} - Image {self.imageID}"

