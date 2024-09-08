from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
import base.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('room/<int:pk>/', views.room, name='room'),
    path('create-room', views.create_room, name='create_room'),
    path('update-room/<int:pk>/', views.update_room, name='update_room'),
    path('delete-room/<int:pk>/', views.delete_room, name='delete_room'),
]
