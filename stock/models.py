from django.db import models
from django.utils import timezone


class File(models.Model):
    file = models.FileField(upload_to='files')
    filename = models.CharField(max_length=100)
    date_uploaded = models.DateTimeField(default=timezone.now)


class Result(models.Model):
    data = models.TextField(max_length=100000)
    file1 = models.ForeignKey(File, on_delete=models.CASCADE, related_name='file1')
    file2 = models.ForeignKey(File, on_delete=models.CASCADE, related_name='file2')
    date_created = models.DateTimeField(default=timezone.now)






