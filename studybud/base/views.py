from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm

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

def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {'form': form}
    return render(request, "create_room.html", context)