from django.db import models


class Classroom(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=11, default='')
    description = models.TextField(max_length=255, blank=True, null=False, default='')
    schedule = models.ImageField(upload_to='uploads/schedule_%Y_%m_%d', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=255)
    group_name = models.CharField(max_length=100)

    classroom = models.ForeignKey('classroom.Classroom', on_delete=models.CASCADE, default='', related_name='channels')

    def __str__(self):
        return self.name
