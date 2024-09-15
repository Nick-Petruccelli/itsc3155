from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Room, Topic
from .forms import RoomForm


# Create your views here.
def home(request) -> HttpResponse:
    q = request.GET.get('q')
    if q:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(desc__icontains=q)
            )
    else:
        rooms = Room.objects.all()
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {"rooms":rooms, "topics":topics, "room_count":room_count}
    return render(request, "home.html", context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usr = User.objects.get(username=username)
        except:
            messages.error(request, "Could not find user")
        
        usr = authenticate(request, username=username, password=password)
        if usr:
            login(request, usr)
            return redirect("/")
    context = {}
    return render(request, "login_register.html", context)

def logoutUser(request):
    logout(request)
    return redirect("/")

def room(request, pk) -> HttpResponse:
    rooms = Room.objects.all()
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