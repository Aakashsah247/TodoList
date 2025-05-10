from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoItem
from .forms import TodoForm

def todo_list(request):
    todos = TodoItem.objects.all().order_by('-created_at')
    total = todos.count()
    completed = todos.filter(completed=True).count()
    progress = int((completed/total)*100) if total > 0 else 0
    
    return render(request, 'todo/todo_list.html', {
        'todos': todos,
        'progress': progress
    })

def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todo/add_todo.html', {'form': form})

def edit_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/edit_todo.html', {'form': form})

def confirm_delete(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    return render(request, 'todo/confirm_delete.html', {'todo': todo})

def delete_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    if request.method == 'POST':
        todo.delete()
    return redirect('todo_list')

def toggle_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')