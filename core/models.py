from django.db import models
import os
from django.utils import timezone

def upload_path(instance, filename):
    name, ext = os.path.splitext(filename)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f"files/{name}_{timestamp}{ext}"

# Create your models here.
class Upload(models.Model):
    file = models.FileField(upload_to=upload_path)
    time= models.DateTimeField(auto_now_add=True)
    extract = models.TextField(blank=True, null = True)

    def __str__(self):
        return self.file.name
    

class ChatHistory(models.Model):
    document = models.ForeignKey(Upload, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    asked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.question[:30]}"

