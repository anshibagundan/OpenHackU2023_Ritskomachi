from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView
from .models import Todo, TodoDay
from .forms import TodoForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views import View
from . import mixins
from datetime import date


class TodoList(ListView):
    model = Todo
    context_object_name = "tasks"


class TodoDetail(DetailView):
    model = Todo
    context_object_name = "task"


class TaskListView(ListView, mixins.MonthCalendarMixin):
    model = Todo
    template_name = 'todo/todo_home.html'
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class TodoUpdate(UpdateView):
    model = Todo
    fields = "__all__"
    success_url = '../..'

    def form_valid(self, form):
        print("form_valid method called")

        response = super().form_valid(form)


        todo_day = get_object_or_404(TodoDay, todo=self.object)
        print(f"Found TodoDay entry: {todo_day.id}")


        todo_day.title = self.object.title
        todo_day.description = self.object.description
        todo_day.deadline = self.object.deadline
        todo_day.importance = self.object.importance
        print(f"Updating TodoDay entry: {todo_day.id} with importance: {todo_day.importance}")

        todo_day.save()

        return response


class BulkDeleteTasks(View):
    template_name = 'todo/todo_confirm_delete.html'

    def post(self, request):
        task_ids = request.POST.getlist('task_ids')
        tasks_to_delete = Todo.objects.filter(id__in=task_ids)

        if 'confirm' in request.POST:
            tasks_to_delete.delete()
            return redirect('list')

        context = {
            'tasks': tasks_to_delete
        }
        return render(request, self.template_name, context)


class TodoCalender(ListView, mixins.MonthCalendarMixin):
    model = Todo
    template_name = 'todo/todo_calender.html'
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class TodoCategory(ListView):
    model = Todo
    template_name = 'todo/todo_category.html'
    context_object_name = "tasks"

def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save()

            TodoDay.objects.create(
                todo=todo,
                title=todo.title,
                description=todo.description,
                deadline=todo.deadline,
                importance=todo.importance
            )

            return redirect('list')
    else:
        form = TodoForm()
    return render(request, 'todo/todo_form.html', {'form': form})

def todo_list(request):
    today = date.today()
    todos = TodoDay.objects.all()

    def custom_sort(todo):
        days_difference = (todo.deadline - today).days
        if days_difference < 0:
            importance_mapping = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}
            importance_value = importance_mapping.get(todo.importance, todo.importance)
        else:
            importance_value = todo.importance
        return importance_value * days_difference

    sorted_todos = sorted(todos, key=custom_sort)

    context = {
        'todos': sorted_todos
    }

    return render(request, 'todo/todo_list.html', context)



def update_tododay(sender, instance, **kwargs):
    TodoDay.objects.update_or_create(
        todo=instance,
        defaults={
            'title': instance.title,
            'description': instance.description,
            'deadline': instance.deadline,
            'importance': instance.importance
        }
    )

def transform_importance(importance):
    return 6 - importance

def todo_importance(request):
    todos_sorted_by_importance = Todo.objects.all().order_by('importance')
    context = {
        'todos': todos_sorted_by_importance
    }
    return render(request, 'todo/todo_importance.html', context)
