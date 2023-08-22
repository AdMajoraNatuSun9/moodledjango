from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('adminpage/', views.adminPage, name='adminpage'),
    path('teacherpage/', views.teacherPage, name='teacherpage'),
    path('studentpage/', views.studentPage, name='studentpage'),
]
