from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm


# Create your views here.
def home(request) -> HttpResponse:
    rooms = Room.objects.all()
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

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, "create_room.html", context)

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('/')
    context = {'obj': 'room'}
    return render(request, "delete.html", context)