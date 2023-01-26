import mimetypes
import os
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import userInfo
from .forms import loginForm, registerForm
from django.http import HttpResponse, FileResponse
from django.core.cache import cache




def home_page(req):
    if 'authin' not in req.session:
        req.session['authin'] = False
        req.session['username'] = 'None'
        
    data = cache.get('data')     
    if not data:
        data = userInfo.objects.all().order_by('-total_score') 
   
    return render(req, 'home.html', {'data':data, 'auth': req.session['authin'], 'username':req.session['username']})

def order_list(req, order='-total_score'):
    data = userInfo.objects.all().order_by(order) 
    cache.set('data', data)
    return redirect('/')         

def register_page(req):
    if 'authin' not in req.session:
        req.session['authin'] = False
        req.session['username'] = 'None'

    if req.method == 'POST':
        form = registerForm(req.POST)
    else:    
        form = registerForm()

    if req.method == 'POST':
        form = registerForm(req.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form .cleaned_data['password_confirm']:
                form.save()
                req.session['authin'] = True
                req.session['username'] = form.cleaned_data['username']
                return redirect('users', name=form.cleaned_data['username'])
            else:
                return render(req, 'register.html', {'register_form':form, 'auth': req.session['authin'], 'username':req.session['username'], 'error':'password and confirmed password not equal'})    
        else:       
                return render(req, 'register.html', {'register_form':form, 'auth': req.session['authin'], 'username':req.session['username']})    
        
    return render(req, 'register.html', {'register_form':form, 'auth': req.session['authin'], 'username':req.session['username']})    

def login_page(req):
    if 'authin' not in req.session:
        req.session['authin'] = False
        req.session['username'] = 'None'

    if req.method == 'POST':
        form = loginForm(req.POST)
    else:    
        form = loginForm()

    if req.method == 'POST':
        form = loginForm(req.POST)
        if form.is_valid():
            try:
                user = userInfo.objects.get(email=form.cleaned_data['email'], password=form.cleaned_data['password']) 
                req.session['authin'] = True
                req.session['username'] = user.username
                return redirect('users', name=user.username)
            except userInfo.DoesNotExist:
                form = loginForm()                  
                return render(req, 'login.html', {'login_form':form, 'auth': req.session['authin'], 'username':req.session['username'], 'error':'email or password not correct!'})
                    
    return render(req, 'login.html', {'login_form':form, 'auth': req.session['authin'], 'username':req.session['username']})


def user_page(req, name):

    if 'authin' in req.session and req.session['authin'] == True:
        user = userInfo.objects.get(username=name)
        return render(req, 'user.html',{'user':user, 'auth': req.session['authin'], 'username': req.session['username']})
    else:
        return redirect('login')

def log_out(req):
    del req.session['authin']
    del req.session['username']
    return redirect('home')        


def download_file(req):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'Space-invader.zip'
    filepath = BASE_DIR + '\\userPage\\static\\' + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response