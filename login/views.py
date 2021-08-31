from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_usr
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.db import connection
# from django.http import HttpResponse

def username_exists(usr):
    if User.objects.filter(username=usr).exists():
        return True
    return False

def reg(usr,pwd):
    if username_exists(usr) == True:
        return False
    user = User.objects.create_user(usr,password=pwd)
    user.save()
    return True

def register(request):
    if request.user.is_authenticated:
        return redirect('../')
    if request.method == 'POST':
        usr = request.POST.get('username',False)
        password = request.POST.get('pwd1')
        f = reg(usr,password)
        if f == True:
            user = authenticate(username=usr, password=password)
            if user is not None and user.is_active:
                login_usr(request, user)
                return redirect('../')
        else:
            return render(request, "index.html",{'taken':True,'stylereg':'visibility: visible','stylelog':'visibility: hidden'})
    else:
        return render(request, "index.html",{'stylereg':'visibility: visible','stylelog':'visibility: hidden'})

def forget(request):
    return render(request, "forget.html")

def login(request):
    if request.user.is_authenticated:
        return redirect('../')
    if request.method == 'POST':
        usr = request.POST.get('username',False)
        password = request.POST.get('pwd')
        if username_exists(usr) == False:
            return render(request, "index.html",{'mismatch':True,'stylelog':'visibility: visible','stylereg':'visibility: hidden'})
        user = authenticate(username=usr, password=password)
        if user is not None and user.is_active:
            login_usr(request, user)
            return redirect('../')
        else:
            return render(request, "index.html",{'mismatch':True,'stylelog':'visibility: visible','stylereg':'visibility: hidden'})
    else:
        return render(request, "index.html",{'stylelog':'visibility: visible','stylereg':'visibility: hidden'})

# def logn(request):
#     form = AuthenticationForm()
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             login_usr(request, form.get_user())
#             return redirect('../')
#         else:
#             print(form.errors)
#     return render(request, 'logn.html', {'form': form})

# def sign_up(request):
#     form = UserCreationForm()
#     if request.method == 'POST':
#         form = UserCreationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('../login/')
#         else:
#             print(form.errors)
#     return render(request, 'sign_up.html', {'form': form})