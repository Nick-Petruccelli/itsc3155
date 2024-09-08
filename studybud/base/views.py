from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

rooms = Room.objects.all()
# Create your views here.
def home(request) -> HttpResponse:
    return render(request, "home.html", {"rooms":rooms})

def room(request, pk) -> HttpResponse:
    room = None
    for i in rooms:
        if i.id == pk:
            room = i
    context = {'room': room}
    return render(request, "room.html", context=context)