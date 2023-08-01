from django.contrib.admin import site

from .models import Task

# Register your models here.

site.register(Task)
