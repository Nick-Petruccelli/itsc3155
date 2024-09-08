from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
import base.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('room/<int:pk>/', views.room, name='room')
]
