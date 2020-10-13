from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    context = {
        'all_users': User.objects.all()
    }

    return render(request,'index.html',context)

def register(request):
    errors = User.objects.validator(request.POST)
    if len (errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
        logged_user = User.objects.create(first_name = request.POST['first_name'],last_name = request.POST['last_name'],email = request.POST['email'],password = pw_hash)
        request.session['userid'] = logged_user.id
        request.session['userfirst'] = logged_user.first_name
        request.session['access'] = 'registered'
        return redirect('/success')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            request.session['userfirst'] = logged_user.first_name
            request.session['access'] = 'logged in'
            return redirect('/success')

    messages.error(request,"User or password is incorrect")
    return redirect('/')

def success(request):
    try:
        request.session['userid']
    except:
        return redirect('/')
    else:
        return render(request,'success.html')
        

def logout(request):
    request.session.clear()
    return redirect('/')