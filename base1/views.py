from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, messages
from .forms import RoomForm, TopicForm
# Create your views here.

def LoginPage(request):
    page = 'login'
    if request.method == "POST":
        print("POST request received")
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exists")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exists')


    context = {'page': page}
    return render(request, 'base1/login_register.html', context)

def RegisterPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

    context = {'form' : form}
    return render(request, 'base1/login_register.html', context)

def LogoutPage(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
        )

    topics = Topic.objects.all()
    count_rooms = rooms.count()
    room_messages = messages.objects.filter(
        Q(room__topic__name__icontains = q)
    )

    context = {"rooms": rooms, "topics": topics, "count_rooms": count_rooms, "room_messages":room_messages}
    return render(request,'base1/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.messages_set.all().order_by('-createds')

    if request.method == "POST":
        room_message = messages.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)  # Redirect after POST instead of using render

    context = {'room': room, 'room_messages': room_messages}
    return render(request, 'base1/room.html', context)

def UserProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.messages_set.all()
    context = {"user":user, "rooms":rooms, "topics":topics, "room_messages":room_messages}
    return render(request, 'base1/profile.html', context)

@login_required(login_url = 'login-page')
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    
    context = {'form':form}
    return render(request, 'base1/room_form.html', context)

@login_required(login_url = 'login-page')
def update_room(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base1/room_form.html', context)

@login_required(login_url = 'login-page')
def delete_room(request, pk):
    room = Room.objects.get(id = pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here")
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base1/delete.html', {'obj':room})

@login_required(login_url = 'login-page')
def delete_message(request, pk):
    room_message = messages.objects.get(id = pk)

    if request.user != room_message.user:
        return HttpResponse("You are not allowed here")
    
    if request.method == "POST":
        room_message.delete()
        return redirect('home')
    return render(request, 'base1/delete.html', {'obj':room_message})

def create_topic(request):
    form = TopicForm()
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid:
            form.save()
        return redirect('home')
    context = {'form':form}
    return render(request, 'base1/new_topic.html', context)