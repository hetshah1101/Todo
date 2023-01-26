from django.shortcuts import render, get_object_or_404
from .forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def get_showing_todos(request, todos):
    if request.GET and request.GET.get('filter'):
        if request.GET.get('filter') == 'completed':
            return todos.filter(is_completed=True)
        if request.GET.get('filter') == 'incomplete':
            return todos.filter(is_completed=False)
    return todos

def index(request):
    todos = Todo.objects.all()
    
    completed_count = todos.filter(is_completed=True).count()
    all_count = todos.count()
    incomplete_count = all_count - completed_count

    context = {'todos': get_showing_todos(request, todos), 
            'completed_count':completed_count, 
            'incomplete_count': incomplete_count,
            'all_count':all_count}

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
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo}
    return render(request, 'todo/todo-detail.html', context)

def todo_delete(request, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo}

    if request.method == 'POST':
        todo.delete()
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'todo/todo-delete.html', context)

def todo_edit(request, id):
    todo = get_object_or_404(Todo, pk=id)
    form = TodoForm(instance=todo)
    context = {'todo': todo, 'form':form}

    if request.method == 'POST':
        titles = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)

        todo.title = titles
        todo.description = description
        todo.is_completed = True if is_completed=="on" else False
        todo.save()

        return HttpResponseRedirect(reverse('todo-detail', kwargs={'id': todo.pk}))

    return render(request, 'todo/todo-edit.html', context)

