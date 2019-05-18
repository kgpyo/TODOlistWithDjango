from datetime import date

from django.db import models
from django.utils import timezone
from django.urls import reverse
from .queryset import *
# Create your models here.
class TodoList(models.Model):
    PRIORITY_CHOICES = [
        (1,'일반'),
        (2,'중요'),
        (3,'긴급'),
        (4,'중요/긴급')
    ]

    objects = TodoListQuerySet.as_manager()

    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, default='')
    write_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deadline = models.DateField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ['-priority', '-write_date']

    def __str__(self):
        return self.title

    def is_finish(self):
        return True if self.is_done == True else False

    def is_deadline_over(self):
        return (self.is_finish() != False) and \
            (self.deadline != None) and \
            (date.today() > self.deadline)

            
    is_finish.BooleanField = True
    is_deadline_over.BooleanField = True