from django.contrib import admin
from .models import *

class TodoListAdmin(admin.ModelAdmin):
    list_display = ('title','write_date','deadline')

admin.site.register(TodoList, TodoListAdmin)
