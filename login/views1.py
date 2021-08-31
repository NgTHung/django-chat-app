from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_usr
from django.db import connection
from django.http import HttpResponse

def username_exists(usr):
    if User.objects.filter(username=usr).exists():
        return True
    return False

def reg(usr,pwd,eml):
    if username_exists(usr) == True:
        return False
    user = User.objects.create_user(usr,eml,pwd)
    user.save()
    return True

def register(request):
    if request.user.is_authenticated:
        return redirect('../')
    if request.method == 'POST':
        usr = request.POST.get('username',False)
        password = request.POST.get('pwd1')
        password2 = request.POST.get('pwd2',False)
        eml = request.POST.get('eml',False)
        csr = connection.cursor()
        csr.execute('use BBQ$usrpwd')
        csr.execute('INSERT INTO id(username) VALUES (%s)', [usr])
        csr.execute('select * from id where username = %s', [usr])
        o = csr.fetchall()[0][1]
        csr.execute('use BBQ$note')
        csr.execute('''CREATE TABLE `%s` (
                    `id` INT AUTO_INCREMENT PRIMARY KEY,
                    `title` TEXT NOT NULL,
                    `body` TEXT NOT NULL,
                    `dt` DATE)''', [o])
        csr.execute('use BBQ$usrpwd')
        connection.commit()
        f = reg(usr,password,eml)
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

def test(request):
    return render(request, "test.html",{'test':'<p class=\"html\">hello</p>'})
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