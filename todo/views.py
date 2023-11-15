from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView
from .models import Todo, TodoDay,Tag,Color
from .forms import TodoForm
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
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login




def title_page(request):
    return render(request, 'todo/todo_title.html')

class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/usercreation_form.html'


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # ログインに成功した場合のリダイレクト先
            return redirect('list')
        else:
            # 認証失敗の場合のエラーメッセージ
            context = {'error': 'ユーザー名またはパスワードが違います'}
            return render(request, 'todo/login.html', context)
    return render(request, 'todo/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('title')


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


class TodoUpdate(LoginRequiredMixin,UpdateView):
    model = Todo
    form_class = TodoForm
    success_url = '../..'


    def get_form_kwargs(self):
        kwargs = super(TodoUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user  # ログインユーザをキーワード引数として追加
        return kwargs
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

@login_required
def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST, user=request.user)

        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()

            tododay = TodoDay(
                todo=todo,
                tag=todo.tag,
                title=todo.title,
                description=todo.description,
                deadline=todo.deadline,
                importance=todo.importance,
                user=request.user  # ここを修正
            )
            tododay.save()  # この行を追加

            return redirect('list')
    else:
        form = TodoForm(user=request.user)
    return render(request, 'todo/todo_form.html', {'form': form})


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


@login_required
def todo_list(request):
    today = date.today()
    todos = TodoDay.objects.filter(user=request.user)


    def custom_sort(todo):
        days_difference = (todo.deadline - today).days
        if days_difference < 0:
            return todo.importance
        elif days_difference == 0:
            return 6 * todo.importance
        else:
            days_difference += 6
            return todo.importance * days_difference

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

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color_id']

@login_required
def Todocategory(request):
    if request.method == 'POST':
        tag_name = request.POST.get('tag-name')
        color_id = request.POST.get('color_id')

        # データベースに新しいTagを保存
        new_tag = Tag(
            name=tag_name,
            color_id_id=color_id,
            is_active=False,
            user=request.user)

        new_tag.save()

        return redirect('category')  # タグを保存した後、同じページにリダイレクト

    colors = Color.objects.filter(user_id=request.user.id)
    tags = Tag.objects.filter(user=request.user.id)
    context = {
        'colors': colors,
        'tags': tags
    }
    return render(request, 'todo/todo_category.html', context)
@csrf_exempt
@login_required
def update_tag_name(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tag_id = data.get('tag_id')
        new_name = data.get('new_name')

        try:
            tag = Tag.objects.get(pk=tag_id, user=request.user.id)
            tag.name = new_name
            tag.save()
            return JsonResponse({"success": True, "message": "タグの名前が更新されました。"})
        except ObjectDoesNotExist:
            # 指定されたタグが存在しない場合のエラーハンドリング
            return JsonResponse({"success": False, "error": "指定されたタグが存在しません。"})
@csrf_exempt
@login_required
def update_tag_color(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tag_id = data.get('tag_id')
        color_id = data.get('color_id')


        try:
            tag = Tag.objects.get(pk=tag_id, user=request.user)
            color_instance = Color.objects.get(pk=color_id)
            tag.color_id = color_instance
            tag.save()
            color = Color.objects.get(pk=color_id)
            return JsonResponse({"success": True, "message": "タグの色が更新されました。",'color_name': color.name})
        except ObjectDoesNotExist:
            return JsonResponse({"success": False, "message": "指定されたタグが存在しません。"})

@csrf_exempt
@login_required
def toggle_tag_activity(request):
    if request.method == "POST":
        tag_id = request.POST.get('tag_id')
        is_active = request.POST.get('is_active') == 'true'

        tag = Tag.objects.get(pk=tag_id, user=request.user)
        tag.is_active = not tag.is_active
        tag.save()

        return JsonResponse({"success": True, "message": "タグの活動状態が変更されました。"})

@csrf_exempt
@login_required
def delete_todo_and_tag(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tag_id = data.get("tag_id")

        try:
            TodoDay.objects.filter(tag=tag_id).delete()
            # 該当のtag_idを持つタスクをすべて削除
            Todo.objects.filter(tag=tag_id).delete()

            # タグ自体を削除
            Tag.objects.get(pk=tag_id).delete()

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
