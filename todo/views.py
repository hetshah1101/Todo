from django.shortcuts import render
from .forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    todos = Todo.objects.all()
    context = {'todos': todos}
    return render(request, 'todo/index.html', context)

def create_todo(request):
    form = TodoForm()
    context = {'form':form}

    if request.method == 'POST':
        titles = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)

        todo = Todo()
        todo.title = titles
        todo.description = description
        todo.is_completed = True if is_completed=="on" else False
        todo.save()

        return HttpResponseRedirect(reverse('todo-detail', kwargs={'id': todo.pk}))

    return render(request, 'todo/create-todo.html', context)

def todo_detail(request, id):
    return render(request, 'todo/todo-detail.html', {})