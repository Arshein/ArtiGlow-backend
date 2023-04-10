from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    description = models.CharField(max_length=256)
    image = models.ImageField(upload_to='images/% Y/% m/% d/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']