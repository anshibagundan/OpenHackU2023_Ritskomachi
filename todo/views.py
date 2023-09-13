from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView
from .models import Todo, TodoDay
from .forms import TodoForm, TagForm
from django.shortcuts import get_object_or_404
from django.views import View
from . import mixins
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth import logout


def title_page(request):
    return render(request, 'todo/todo_title.html')

class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/usercreation_form.html'


@login_required
def logout_view(request):
    logout(request)
    return redirect('title')

@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user)

    context = {
        'todos': todos
    }
    return render(request, 'todo_list.html', context)

class TodoDetail(LoginRequiredMixin, DetailView):
    model = Todo
    context_object_name = "task"

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class TaskListView(LoginRequiredMixin, ListView, mixins.MonthCalendarMixin):
    model = Todo
    template_name = 'todo/todo_home.html'
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)



class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = "__all__"
    success_url = '../..'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Todo オブジェクトから TodoDay エントリを取得
        todo_day = get_object_or_404(TodoDay, todo=self.object)

        # importance フィールドを正しく設定
        todo_day.importance = self.object.importance

        # 他のフィールドも必要に応じて更新

        # TodoDay エントリを保存
        todo_day.save()

        return response



class BulkDeleteTasks(LoginRequiredMixin, View):
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


class TodoCalender(LoginRequiredMixin, ListView, mixins.MonthCalendarMixin):
    model = Todo
    template_name = 'todo/todo_calender.html'
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class TodoCategory(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/todo_category.html'
    context_object_name = "tasks"

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


@login_required
def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)

        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()

            TodoDay.objects.create(
                todo=todo,
                user=request.user,
                title=todo.title,
                description=todo.description,
                deadline=todo.deadline,
                importance=todo.importance,
                tag=todo.tag if todo.tag else None
            )
            return redirect('list')
    else:
        form = TodoForm()

    return render(request, 'todo/todo_form.html', {'form': form})

@login_required
def todo_list(request):
    today = date.today()
    todos = TodoDay.objects.filter(user=request.user)


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


@login_required
def update_tododay(sender, instance, **kwargs):
    TodoDay.objects.update_or_create(
        todo=instance,
        defaults={
            'title': instance.title,
            'description': instance.description,
            'deadline': instance.deadline,
            'importance': instance.importance,
            'tag': instance.tag,
}
    )
def transform_importance(importance):
    return 6 - importance

@login_required
def todo_importance(request):
    todos_sorted_by_importance = Todo.objects.filter(user=request.user).order_by('importance')

    context = {
        'todos': todos_sorted_by_importance
    }
    return render(request, 'todo/todo_importance.html', context)

@login_required
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect('list')
    else:
        form = TagForm()
    return render(request, 'todo_list.html', {'form': form})
