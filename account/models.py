from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
User = settings.AUTH_USER_MODEL


class ProjectDetails(models.Model):
    username = models.CharField(max_length=50)
    taskName = models.CharField(max_length=50)
    projectName = models.CharField(max_length=50)
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return self.username
