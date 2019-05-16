from django.urls import path
from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:todo_id>', views.TodoListContentView.as_view(), name='todo'),
    path('done', views.TodoListDoneView.as_view(), name='done'),
    path('deadline-is-over', views.TodoListDeadLineIsOverView.as_view(), name='deadline'),
    path('to-do', views.TodoListView.as_view(), name='todolist'),
]