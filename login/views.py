import socketio
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_usr

# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.db import connection
# from django.http import HttpResponse
sio = socketio.Server(async_mode="gevent")
thread = None


def chat(request):
    if not request.user.is_authenticated:
        return redirect("../login/")
    return render(request, "chat.html")


def username_exists(usr):
    if User.objects.filter(username=usr).exists():
        return True
    return False


def reg(usr, pwd):
    if username_exists(usr) == True:
        return False
    user = User.objects.create_user(usr, password=pwd)
    user.save()
    return True


def register(request):
    if request.user.is_authenticated:
        return redirect("../")
    if request.method == "POST":
        usr = request.POST.get("username", False)
        password = request.POST.get("pwd1")
        f = reg(usr, password)
        if f == True:
            user = authenticate(username=usr, password=password)
            if user is not None and user.is_active:
                login_usr(request, user)
                return redirect("../")
        else:
            return render(
                request,
                "index.html",
                {
                    "taken": True,
                    "stylereg": "visibility: visible",
                    "stylelog": "visibility: hidden",
                },
            )
    else:
        return render(
            request,
            "index.html",
            {"stylereg": "visibility: visible", "stylelog": "visibility: hidden"},
        )


def forget(request):
    return render(request, "forget.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("../")
    if request.method == "POST":
        usr = request.POST.get("username", False)
        password = request.POST.get("pwd")
        if username_exists(usr) == False:
            return render(
                request,
                "index.html",
                {
                    "mismatch": True,
                    "stylelog": "visibility: visible",
                    "stylereg": "visibility: hidden",
                },
            )
        user = authenticate(username=usr, password=password)
        if user is not None and user.is_active:
            login_usr(request, user)
            return redirect("../")
        else:
            return render(
                request,
                "index.html",
                {
                    "mismatch": True,
                    "stylelog": "visibility: visible",
                    "stylereg": "visibility: hidden",
                },
            )
    else:
        return render(
            request,
            "index.html",
            {"stylelog": "visibility: visible", "stylereg": "visibility: hidden"},
        )


@sio.event
def id(sid, data):
    print("id: " + sid)
    print("data: " + data)


@sio.event
def connect(sid, data):
    print("id: " + sid)
    print(data)
