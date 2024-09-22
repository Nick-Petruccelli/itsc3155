from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm


# Create your views here.
def home(request) -> HttpResponse:
    q = request.GET.get('q') if request.GET.get('q') != None else ''
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
    room_messages = Message.objects.filter(Q(room__name__icontains=q))
    context = {"rooms":rooms, "topics":topics, "room_count":room_count, "room_messages": room_messages}
    return render(request, "home.html", context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect("/")
    page = "login"
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usr = User.objects.get(username=username)
        except:
            messages.error(request, "Could not find user")
        
        usr = authenticate(request, username=username, password=password)
        if usr != None:
            login(request, usr)
            return redirect("/")
    context = {"page":page}
    return render(request, "login_register.html", context)

def logoutUser(request):

    logout(request)
    return redirect("/")

def registerUser(request):
    if request.user.is_authenticated:
        return redirect("/")
    form = UserCreationForm()
    if request.method == 'POST':
        form = request.POST
        user = User.objects.create(
            username=form.get('username'),
            password=form.get('password')
            )
        login(request, user)
        return redirect("/")
    context = {"form":form}
    return render(request, "login_register.html", context)

def room(request, pk) -> HttpResponse:
    room = Room.objects.get(id=pk)
    msgs = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        print("hit post")
        form = Message.objects.create(msg=request.POST.get('msg'), user=request.user, room=room)
        form.save()
        room.participants.add(request.user)
        return redirect(f"/room/{pk}")
    context = {'room': room, "msgs": msgs, "participants": participants}
    return render(request, "room.html", context=context)

def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'profile.html', context)
@login_required(login_url='/login')
def delete_message(request, pk):
    msg = Message.objects.get(id=pk)
    room_id = msg.room.id
    if request.user == msg.user:
        msg.delete()
        return redirect(f"/room/{room_id}")
    else:
        return HttpResponse('You dont belong here!!!!!!!')

@login_required(login_url='/login')
def create_room(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = request.POST
        if not Topic.objects.filter(name=form.get('topic')).exists():
            Topic.objects.create(name=form.get('topic'))
        Room.objects.create(
            host=request.user,
            name=form.get('room_name'),
            topic=Topic.objects.get(name=form.get('topic')),
            desc=form.get('room_about')
        )
        return redirect('/')
    context = {'topics':topics}
    return render(request, "create_room.html", context)

@login_required(login_url='/login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You dont belong here!!!!!!!')
    
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, "create_room.html", context)

@login_required(login_url='/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You dont belong here!!!!!!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('/')
    context = {'obj': room}
    return render(request, "delete.html", context)

@login_required(login_url="/login")
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        return redirect('user-profile', pk=user.id)
    context = {'form': form}
    return render(request, "update_user.html",context)