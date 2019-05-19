from django.urls import path
from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.MainPageView.as_view(), name='index'),
    path('done', views.TodoListCompleteView.as_view(), name='done'),
    path('expired', views.TodoListExpiredView.as_view(), name='expired'),
    path('to-do-list', views.TodoListIncompleteView.as_view(), name='todolist'),
    path('all', views.TodoListAllView.as_view(), name='all'),

    path('<int:todo_id>', views.TodoListDetailView.as_view(), name='detail'),
    path('<int:todo_id>/complete', views.complete, name='complete'),
    path('<int:todo_id>/incomplete', views.incomplete, name='incomplete'),
]