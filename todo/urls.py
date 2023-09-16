from django.urls import path,include
from .views import TodoDetail,TaskListView,  BulkDeleteTasks,TodoUpdate, TodoCalender, TagForm ,todo_importance,logout_view
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.title_page, name='title'),
    path('list/', views.todo_list, name='list'),
    path('importance/', todo_importance, name='todo_importance'),
    path('detail/<int:pk>/', TodoDetail.as_view(), name='detail'),
    path('todo_home/', TaskListView.as_view(), name='todo_home'),
    path('update/<int:pk>/', TodoUpdate.as_view(), name='update'),
    path('delete/', BulkDeleteTasks.as_view(), name='delete'),
    path('todo_category/', views.Todocategory,name='category'),
    path('todo_category/update_tag_name/', views.update_tag_name, name='update_tag_name'),
    path('todo_category/update_tag_color/', views.update_tag_color, name='update_tag_color'),
    path('todo_category/toggle_tag_activity/', views.toggle_tag_activity, name='toggle_tag_activity'),
    path('delete_tag_and_todo/', views.delete_todo_and_tag, name='delete_tag_and_todo'),
    path('todo_calender/<int:year>/<int:month>/',TodoCalender.as_view(), name='calender'),
    path('todo_addtask/', views.create_todo, name='create_todo'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', logout_view, name='logout'),



]
urlpatterns += staticfiles_urlpatterns()
