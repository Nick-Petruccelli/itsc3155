from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request) -> HttpResponse:
    return HttpResponse('Home Page')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
]
