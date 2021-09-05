from typing import Tuple
from django.db.models.expressions import F
import socketio
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_usr
from login.models import USID, Message, midroom
from login.models import friends as Friends
import random, string


# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.db import connection
# from django.http import HttpResponse
sio = socketio.Server(async_mode="gevent")
thread = None
username = ""
# session = None


def chat(request, room):
    if not request.user.is_authenticated:
        return redirect("../login/")
    global username
    username = request.user.username
    db = Friends.objects.get(requester=username)
    friends_list = db.friend_list
    friends = friends_list.split()
    rooms = midroom.objects.get(first_person=username)
    mess_list = Message.objects.filter(receiver=rooms).values_list('sender','messages')
    return render(request,'chat.html',{'friends': friends, 'mess_list': mess_list})


def wrong(request):
    if not request.user.is_authenticated:
        return redirect("../login/")
    global username
    username = request.user.username
    db = Friends.objects.get(requester=username)
    friends_list = db.friend_list
    friends = friends_list.split()
    return render(request,'chat.html',{'friends': friends})



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
            db = USID.objects.create(username=usr)
            friends_list = Friends.objects.create(requester=usr,friend_list='')
            friends_list.save()
            db.save()
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
def chatrooms(sid, chatroom, username):
    if chatroom == 'chatall':
        sio.enter_room(sid=sid, room='chatall')
        print('connected to chatall')
        return False
    room = midroom.objects.get(first_person=username).theroom
    sio.enter_room(sid=sid, room=room)
    print('connected to ' + room)
    

# @sio.event
# def id(sid):
    # global session


@sio.event
def connected(sid, data, username, room=None):
    print(username)
    db = USID.objects.get(username=username)
    db.sid = sid
    db.save()
    sio.save_session(sid, {"username": username, "sid": sid, 'chatroom': room})


@sio.event
def prints(sid, data, username, room = None):
    # global session
    data = data.strip()
    print(f"{username} says: {data}")
    mess = Message.objects.create(
        sender=username, receiver=room, messages=data
    )
    mess.save()
    sio.emit(
        'get', f'{username} says: {data}\n', to=room)


@sio.event
def add_friend(sid, friend):
    try:
        session = sio.get_session(sid)
        # global username
        username = session['username']
        an_db = Friends.objects.get(requester=friend)
        if session['username'] in an_db.friend_list:
            sio.emit('resp', 'false: already in friend list', room=sid)
            return False
        an_db.friend_list += ' '+username
        an_db.save()
        db = Friends.objects.get(requester=username)
        if friend in db.friend_list:
            sio.emit('resp', 'false: already in friend list', room=sid)
            return False
        db.friend_list += friend
        db.save()
        sio.emit('resp','success', room=sid)
        rom = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(30))
        rdb = midroom.objects.create(first_person=username,theroom= rom)
        sec_rdm = midroom.objects.create(first_person=friend,theroom= rom)
        rdb.save()
        sec_rdm.save()
    except Exception as error:
        sio.emit('resp', str(error))

@sio.event
def getroom(sid,data):
    if data == 'chatall':
        return False
    chatroom = midroom.objects.get(first_person=data).theroom
    sio.emit('desroom',chatroom)