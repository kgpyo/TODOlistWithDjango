from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.views import generic
from dateutil.parser import parse

from .models import *
from .forms import *
"""
메인페이지, 글 작성 처리
"""
class MainPageView(generic.View):
    def get(self, request):
        form = TodoListForm()
        return render(request, 
            'todo/form.html', 
            {'form':form},
        )
    
    def post(self, request):
        form = TodoListForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            return HttpResponseBadRequest(form.errors.as_data().values())
        return HttpResponseRedirect(reverse('todo:index'))

"""
세부정보 뷰, 글 수정, 읽기, 삭제 편집
"""
# pk 값을 이용한 데이터 처리 클래스뷰        
class TodoListDetailView(generic.View):
    # html, form에서 put, delete method 사용을 위한 편법처리
    # _method == put, delete로 구분
    def post(self, request, todo_id):
        method = request.POST.get('_method', 'none')
        if method.upper() == 'PUT':
            return self.put(request, todo_id)
        if method.upper() == 'DELETE':
            return self.delete(request, todo_id)
        return HttpResponseForbidden()

    def get(self, request, todo_id):
        todolist = get_object_or_404(TodoList, pk=todo_id)
        form = TodoListForm(instance=todolist)
        return render(request, 'todo/form.html', {
            'modify':True,
            'todo_id':todo_id,
            'write_date':todolist.write_date,
            'updated_date':todolist.updated_date,
            'form':form
        })
    
    def put(self, request, todo_id):
        todolist = get_object_or_404(TodoList, pk=todo_id)
        form = TodoListForm(request.POST, instance=todolist)
        if form.is_valid():
            form.save()
        else:
            return HttpResponseBadRequest(form.errors.as_data().values())
        return HttpResponseRedirect(reverse('todo:detail', args=(todo_id,)))

    def delete(self, request, todo_id):
        todolist = get_object_or_404(TodoList, pk=todo_id)
        todolist.delete()
        return HttpResponseRedirect(reverse('todo:index'))


"""
미완료 목록, 완료 목록, 완료하지 못하고 마감기한이 지난 목록 뷰
"""
class TodoListCompleteView(generic.ListView):
    model = TodoList
    context_object_name = 'to_do_list'
    template_name='todo/list_view.html'
    extra_context={'board_name':'완료'}

    def get_queryset(self):
        return TodoList.objects.get_complete_list()

class TodoListExpiredView(generic.ListView):
    model = TodoList
    context_object_name = 'to_do_list'
    template_name='todo/list_view.html'
    extra_context={'board_name':'만료, 하지못한일'}

    def get_queryset(self):
        return TodoList.objects.get_expired_list()

class TodoListIncompleteView(generic.ListView):
    model = TodoList
    context_object_name = 'to_do_list'
    template_name='todo/list_view.html'
    extra_context={'board_name':'할 일 목록'}

    def get_queryset(self):
        return TodoList.objects.get_incomplete_list()

"""
TodoList DB - pk의 완료 혹은 미완료 처리 설정
"""
def complete(request, todo_id):
    todolist = get_object_or_404(TodoList, pk=todo_id)
    todolist.is_done = True
    todolist.save()
    return HttpResponseRedirect(reverse('todo:index'))

def incomplete(request, todo_id):
    todolist = get_object_or_404(TodoList, pk=todo_id)
    todolist.is_done = False
    todolist.save()
    return HttpResponseRedirect(reverse('todo:index'))