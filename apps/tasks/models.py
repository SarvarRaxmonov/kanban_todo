from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    sub_tasks = models.ManyToManyField("SubTask")
    status = models.ForeignKey("Column", on_delete=models.SET_NULL, null=True, related_name="chosen_tasks")

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.TextField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Column(models.Model):
    name = models.CharField(max_length=50)
    board = models.ForeignKey("tasks.Board", on_delete=models.CASCADE, default=1, related_name="chosen_column")

    def __str__(self):
        return self.name


class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
