from django.contrib.auth.models import User
from django.db import models


class Art(models.Model):
    description = models.CharField(max_length=256)
    image = models.ImageField(upload_to='images/% Y/% m/% d/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
