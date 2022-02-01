from django.db import models
from django.contrib.auth.models import User


class Lists(models.Model):
    name = name = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="lists", null=True)
    default = models.BooleanField(default=False)
    order = models.IntegerField(default=100)

    def __str__(self):
        return self.name


class Task(models.Model):
    lists = models.ForeignKey(Lists, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks", null=True)
    name = models.CharField(max_length=100)
    complete = models.BooleanField()
    due_date = models.DateField(null=True)
    important = models.BooleanField(default=False)
    subnote = models.TextField(max_length=200, null=True)

    def __str__(self):
        return self.name
