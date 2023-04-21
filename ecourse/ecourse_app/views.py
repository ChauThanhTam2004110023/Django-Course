from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .forms import CreateUserForm
# Create your views here.

class loginPage(View):
    def get(self, request):
        self.page = "login"
        if self.request.user.is_authenticated:
            return redirect('home')
        context = {
            'page': self.page
        }
        return render(request, 'base/login_register.html', context)
    
    def post(self, request):
        self.page = 'login'
        if self.request.user.is_authenticated:
            return redirect('home')
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist.')
        context = {
            'page': self.page
        }
        return render(request, 'base/login_register.html', context)

    
# class registerPage(View):
#     def get(self, request):
#         self.form = UserCreationForm()
#         context = {
#             'form': self.form
#         }
#         return render(request, 'base/login_register.html', context)
    
#     def post(self, request):
#         self.form = UserCreationForm(self.request.POST)
#         if self.form.is_valid():
#             self.user = self.form.save(commit=False)
#             self.user.username = self.user.username
#             self.user.save()
#             login(request, self.user)
#             return redirect('home')
#         else:
#             messages.error(request, 'An error occurred during registration?')
#         context = {
#             'form': self.form
#         }
#         return render(request, 'base/login_register.html', context)


class registerPage(View):
    def get(self, request):
        self.form = CreateUserForm()
        context = {
            'form': self.form
        }
        return render(request, 'base/created_user.html', context)
    
    def post(self, request):
        self.form = CreateUserForm(self.request.POST)
        if self.form.is_valid():
            self.form.save()
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration?')
        context = {
            'form': self.form
        }
        return render(request, 'base/created_user.html', context)


class logoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class home(View):
    def get(self, request):
        self.q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        self.rooms = Room.objects.filter(
            Q(topic__name__contains=self.q) |
            Q(name__icontains=self.q) |
            Q(descriptions__icontains=self.q))

        self.topics = Topic.objects.all()
        self.room_count = self.rooms.count()
        self.room_messages = Message.objects.filter(Q(room__topic__name__icontains=self.q))
        context = {
            'rooms': self.rooms,
            'topics': self.topics,
            'room_count': self.room_count,
            'room_messages': self.room_messages,
        }
        return render(request, 'base/home.html', context)


class room(View):
    def get(self, request, pk):
        self.room = Room.objects.get(id=pk)
        self.room_messages = self.room.message_set.all()
        self.participants = self.room.participants.all()

        context = {
            'room': self.room,
            'room_messages': self.room_messages,
            'participants': self.participants
        }
        return render(request, 'base/room.html', context)
    
    def post(self, request, pk):
        self.room = Room.objects.get(id=pk)
        self.room_messages = self.room.message_set.all()
        self.participants = self.room.participants.all()
        
        self.message = Message.objects.create(
            user = self.request.user,
            room = self.room,
            body = self.request.POST.get('body')
        )
        context = {
            'room': self.room,
            'room_messages': self.room_messages,
            'participants': self.participants
        }

        return render(request, 'base/room.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class createRoom(View):
    def get(self, request):
        self.form = RoomForm()
        context = {
            "form": self.form
        }
        return render(request, 'base/room_form.html', context)

    def post(self, request):
        self.form = RoomForm(self.request.POST)
        if self.form.is_valid():
            self.room = self.form.save(commit=False)
            self.host = self.request.user
            self.room.save()
            return redirect("home")
        context = {"form": self.form}
        return render(request, 'base/room_form.html', context)



@method_decorator(login_required(login_url='login'), name='dispatch')
class updateRoom(View):
    def get(self, request, pk):
        self.listing = Room.objects.get(id=pk)
        self.form = RoomForm(instance=self.listing)
        context = {
            "form": self.form
        }
        return render(request, 'base/room_form.html', context)
    
    def post(self, request, pk):
        self.listing = Room.objects.get(id=pk)
        self.form = RoomForm(self.request.POST ,instance=self.listing)
        if self.form.is_valid():
            self.form.save()
            return redirect("home")
        context = {
            "form": self.form
        }
        return render(request, 'base/room_form.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class deleteRoom(View):
    def get(self, request, pk):
        self.room = Room.objects.get(id=pk)
        return render(request, 'base/delete.html', {'obj':self.room})
    def post(self, request, pk):
        self.room = Room.objects.get(id=pk)
        if self.request.method == 'POST':
            self.room.delete()
            return redirect('home')
        return render(request, 'base/delete.html', {'obj':self.room})


@method_decorator(login_required(login_url='login'), name='dispatch')
class deleteMessage(View):
    def get(self, request, pk):
        self.message = Message.objects.get(id=pk)
        return render(request, 'base/delete.html', {'obj':self.message})
    def post(self, request, pk):
        self.message = Message.objects.get(id=pk)
        if self.request.method == 'POST':
            self.message.delete()
            return redirect('home')
        return render(request, 'base/delete.html', {'obj':self.message})
    


class userProfile(View):
    def get(self, request, pk):
        self.user = User.objects.get(id=pk)
        self.rooms = self.user.room_set.all()
        self.topics = Topic.objects.all()
        self.room_messages = self.user.message_set.all()

        context = {
            'user': self.user,
            'rooms': self.rooms,
            'topics': self.topics,
            'room_messages': self.room_messages
        }
        return render(request, 'base/profile.html', context)
    