from django.db import models


class USID(models.Model):
    sid = models.CharField(max_length=30)
    username = models.CharField(max_length=256)

    def __str__(self):
        return self.username


class Message(models.Model):
    sender = models.CharField(max_length=256)
    receiver = models.CharField(max_length=256, null=True)
    messages = models.CharField(max_length=1000)

    def __str__(self):
        return self.messages


class friends(models.Model):
    requester = models.CharField(max_length=256)
    friend_list = models.TextField(null=True)

    def __str__(self):
        return self.requester
    
class midroom(models.Model):
    first_person = models.CharField(max_length=256)
    theroom = models.CharField(max_length=50)
    
    def __str__(self):
        return self.theroom
    
