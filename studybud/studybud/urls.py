from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
import base.views as views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('room/<int:pk>/', views.room, name='room'),
    path('profile/<int:pk>/', views.user_profile, name="user-profile"),
    path('create-room', views.create_room, name='create_room'),
    path('update-room/<int:pk>/', views.update_room, name='update_room'),
    path('delete-room/<int:pk>/', views.delete_room, name='delete_room'),
    path('delete-msg/<int:pk>/', views.delete_message, name='delete_msg'),
    path('update_user/', views.update_user, name='update_user'),
    path('topics/', views.topics_page, name='topics'),
    path('activity/', views.activity_page, name='activity'),
    path('api/', include('base.api.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
