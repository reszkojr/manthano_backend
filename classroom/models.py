from django.db import models

from authentication.models import ManthanoUser


class Classroom(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=11, unique=True)
    description = models.TextField(max_length=255, blank=True, null=False, default='')
    schedule = models.ImageField(upload_to='uploads/schedule_%Y_%m_%d', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Channel(models.Model):
    classroom = models.ForeignKey('classroom.Classroom', on_delete=models.CASCADE, default='', related_name='channels')

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(ManthanoUser, related_name='messages', null=True, on_delete=models.SET_NULL)
    channel = models.ForeignKey(Channel, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    date = models.DateField(auto_now_add=True)
    edited = models.BooleanField(default=False)
