from django.urls import path,include, re_path
from .views import TodoDetail,TaskListView, TodoUpdate, BulkDeleteTasks, TodoCalender, TodoCategory, todo_importance,logout_view
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.title_page, name='title'),
    path('list/', views.todo_list, name='list'),
    path('detail/<int:pk>/', TodoDetail.as_view(), name='detail'),
    path('todo_home/', TaskListView.as_view(), name='todo_home'),
    path('update/<int:pk>/', TodoUpdate.as_view(), name='update'),
    path('delete/', BulkDeleteTasks.as_view(), name='delete'),
    path('todo_category/', TodoCategory.as_view(), name='category'),
    path('create_category/', views.create_tag, name='create_category'),
    path('edit_tag/<int:tag_id>/', views.edit_tag, name='edit_tag'),
    path('delete_tag/<int:tag_id>/', views.delete_tag, name='delete_tag'),
    path('todo_calender/<int:year>/<int:month>/',TodoCalender.as_view(), name='calender'),
    path('create/', views.create_todo, name='create_todo'),
    path('importance/', todo_importance, name='todo_importance'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', logout_view, name='logout'),



]
urlpatterns += staticfiles_urlpatterns()
