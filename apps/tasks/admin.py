from django.contrib.admin import site

from .models import Board, Column, SubTask, Task

site.register(Task)
site.register(SubTask)
site.register(Board)
site.register(Column)
