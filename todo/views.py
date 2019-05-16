from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.views import View, generic
from django.db.models import Q
from dateutil.parser import parse
import datetime


from .models import *

# Create your views here.
def index(request):
    #글 작성시
    if request.method == "POST":
        return write_post(request)

    data = {
        'deadline_over_count':0,
        'goal':0.0
        }
    todolist = TodoList.objects.filter(is_done=False, deadline__lt=datetime.date.today())
    
    data['deadline_over_count'] = todolist.count()

    try:
        done = TodoList.objects.filter(is_done=True).count()
        total = TodoList.objects.all().count()
        data['goal'] = (done/total)*100
    except:
        data['goal'] = 0

    return render(request, 'todo/index.html', data)

def write_post(request):
    input_data = {}
    input_data['title'] = request.POST.get('title', None)
    input_data['text'] = request.POST.get('text', "")
    input_data['deadline'] = request.POST.get('deadline', None)
    input_data['priority'] = request.POST.get('priority', 1)
    if input_data['deadline'] and request.POST.get('setDeadline', 0) == "1":
        input_data['deadline'] = parse(input_data['deadline']).date()
    else:
        input_data['deadline'] = None
    todolist = TodoList(**input_data)
    if todolist.is_valid():
        todolist.save()
       
    return HttpResponseRedirect(reverse('todo:index'))

class TodoListDoneView(generic.ListView):
    model = TodoList
    context_object_name = 'to_do_list'
    template_name='todo/list_view.html'

    def get_queryset(self):
        return TodoList.objects.filter(is_done=True)

class TodoListDeadLineIsOverView(generic.ListView):
    model = TodoList
    context_object_name = 'to_do_list'
    template_name='todo/list_view.html'

    def get_queryset(self):
        return TodoList.objects.filter(is_done=False, \
        deadline__lt=datetime.date.today())

class TodoListView(generic.ListView):
    model = TodoList
    context_object_name = 'to_do_list'
    template_name='todo/list_view.html'

    def get_queryset(self):
        return TodoList.objects.filter(
            (Q(deadline__gte=datetime.date.today())&Q(is_done=False))|
            (Q(deadline__isnull=True)&Q(is_done=False))
        )

        
class TodoListContentView(View):
    def post(self, request, todo_id):
        if request.POST['_method'].upper() == 'PUT':
            return self.put(request, todo_id)
        if request.POST['_method'].upper() == 'DELETE':
            return self.delete(request, todo_id)

    def get(self, request, todo_id):
        todolist = get_object_or_404(TodoList, pk=todo_id)
        return render(request, 'todo/content.html', {'content':todolist})
    
    def put(self, request, todo_id):
        todolist = get_object_or_404(TodoList, pk=todo_id)
        todolist.title = request.POST.get('title', todolist.title)
        todolist.text = request.POST.get('text', todolist.text)
        deadline = request.POST.get('deadline', todolist.deadline)
        todolist.priority = request.POST.get('priority',todolist.priority)
        if request.POST.get('setDeadline', 0) == "1":
            todolist.deadline = parse(deadline).date()
        todolist.is_done = request.POST.get('is_done', todolist.is_done)
        if todolist.is_valid():
            todolist.save()
        return HttpResponseRedirect(reverse('todo:index'))
        

    def delete(self, request, todo_id):
        todolist = get_object_or_404(TodoList, pk=todo_id)
        todolist.delete()
        return HttpResponseRedirect(reverse('todo:index'))
