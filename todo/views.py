from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.views import View, generic
from django.db.models import Q
from dateutil.parser import parse
from django.db.models import F
import datetime


from .models import *

def index(request):
    #글 작성시
    if request.method == "POST":
        return write_post(request)
    data = {
        'priority_choices' : TodoList.PRIORITY_CHOICES
    }
    return render(request, 'todo/form.html', data)

def print_error(request, error_code, msg = None):
    if msg is None:
        if error_code == 404:
            msg = "존재하지 않는 게시글이거나 페이지를 찾을 수 없습니다."
        if error_code == 500:
            msg = "처리중 오류가 발생하였습니다."

    return render(request, 
        'todo/error.html', 
        {
            'error_code':error_code, 'error_message':msg
        }
    )

class ProcessError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

def write_post(request):
    try:
        input_data = {
            'title':request.POST.get('title', None),
            'text':request.POST.get('text', ''),
            'deadline': None,
            'priority':request.POST.get('priority', 1)
        }
        deadline = request.POST.get('deadline',None)

        if not input_data['title']:
            raise ProcessError('제목을 입력해주세요')
        if deadline and deadline is not '':
            input_data['deadline'] = parse(deadline)
        else:
            input_data['deadline'] = None
            
    except ProcessError as e:
        return print_error(request, 500, e)
    except:
        return print_error(request, 500)

    todolist = TodoList(**input_data)
    if todolist.is_valid():
        todolist.save()
    else:
        return print_error(request, 400, "잘못된 요청입니다. 입력하신 내용을 다시 한번 확인해주세요.")
       
    return HttpResponseRedirect(reverse('todo:index'))

#리스트 뷰
class TodoListDoneView(generic.ListView):
    model = TodoList
    context_object_name = 'to_do_list'
    template_name='todo/list_view.html'
    board_name = '완료'

    def get_queryset(self):
        return TodoList.objects.filter(is_done=True).\
            order_by('-priority', '-write_date')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['board_name'] = self.board_name
        return data

class TodoListDeadLineIsOverView(generic.ListView):
    model = TodoList
    context_object_name = 'to_do_list'
    template_name='todo/list_view.html'
    board_name = '마감기한  '

    def get_queryset(self):
        return TodoList.objects.filter(is_done=False, \
        deadline__lt=datetime.date.today()).\
            order_by('-priority', '-write_date')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['board_name'] = self.board_name
        return data

class TodoListView(generic.ListView):
    model = TodoList
    context_object_name = 'to_do_list'
    template_name='todo/list_view.html'
    board_name = '할 일 목록'

    def get_queryset(self):
        return TodoList.objects.filter(
            (Q(deadline__gte=datetime.date.today())&Q(is_done=False))|
            (Q(deadline__isnull=True)&Q(is_done=False))
        ).order_by('-priority', '-write_date')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['board_name'] = self.board_name
        return data

# pk 값을 이용한 데이터 처리 클래스뷰        
class TodoListContentView(View):
    def post(self, request, todo_id):
        method = request.POST.get('_method', 'none')
        if method.upper() == 'PUT':
            return self.put(request, todo_id)
        if method.upper() == 'DELETE':
            return self.delete(request, todo_id)
        return HttpResponse("forbiden")

    def get(self, request, todo_id):
        try:
            todolist = TodoList.objects.get(pk=todo_id)
        except TodoList.DoesNotExist:
            return print_error(request, 404)
        return render(request, 'todo/form.html', {
            'content':todolist,
            'priority_choices' : TodoList.PRIORITY_CHOICES
        })
    
    def put(self, request, todo_id):
        try:
            todolist = TodoList.objects.get(pk=todo_id)
        except TodoList.DoesNotExist:
            return print_error(request, 404)
        todolist.title = request.POST.get('title', todolist.title)
        todolist.text = request.POST.get('text', todolist.text)
        todolist.priority = request.POST.get('priority',todolist.priority)
        todolist.is_done = request.POST.get('is_done', todolist.is_done)
        deadline = request.POST.get('deadline',None)

        if deadline and deadline is not '':
            deadline = parse(deadline)
        else:
            deadline = None

        todolist.deadline = deadline
        if todolist.is_valid():
            todolist.save()
        return HttpResponseRedirect(reverse('todo:index'))
        

    def delete(self, request, todo_id):
        try:
            todolist = TodoList.objects.get(pk=todo_id)
        except TodoList.DoesNotExist:
            return print_error(request, 404)
        todolist.delete()
        return HttpResponseRedirect(reverse('todo:index'))

def changeDone(request, todo_id):
    try:
        todolist = TodoList.objects.get(pk=pk)
    except TodoList.DoesNotExist:
        return print_error(request, 404)
    todolist.is_done = True if F('is_done') is False else False
    return HttpResponseRedirect(reverse('todo:index'))