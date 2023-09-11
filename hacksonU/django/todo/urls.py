from django.urls import path
from .views import TodoDetail,TaskListView, TodoUpdate, TodoDelete, TodoCalender, TodoCategory, todo_importance
from . import views

urlpatterns = [
    path("", views.todo_list, name='list'),
    path('detail/<int:pk>/', TodoDetail.as_view(), name='detail'),
    path('todo_home/', TaskListView.as_view(), name='todo_home'),
    path('update/<int:pk>/', TodoUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', TodoDelete.as_view(), name='delete'),
    path('todo_category/', TodoCategory.as_view(), name='category'),
    path('todo_calender/<int:year>/<int:month>/',TodoCalender.as_view(), name='calender'),
    path('create/', views.create_todo, name='create_todo'),
    path('importance/', todo_importance, name='todo_importance'),
]
