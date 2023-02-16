from django.shortcuts import render, redirect
from .models import userInfo, profile
from .forms import loginForm, registerForm, send_reset_Form, change_pass_Form
from django.core.cache import cache
import uuid
from django.core.mail import send_mail
import re


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

def verify(req):
    if req.method == 'GET' and 'token' in req.GET:
        user = profile.objects.get(token=str(req.GET.get('token')))
        if user:
            name = user.username
            req.session['authin'] = True
            req.session['username'] = user.username
            userInfo.objects.create(username=user.username, email=user.email, password=user.password)
            user.delete()
            return redirect('users', name=name)

    return redirect('home')

def send_reset_pass(req):
    if req.method == 'POST':
        form = send_reset_Form(req.POST)
        try:
            if form.is_valid() and userInfo.objects.get(email=form.cleaned_data['email']) != None:
                token = uuid.uuid4().hex
                sub = 'smart space invaders reset password'
                mess = f'click the link to reset your password https://www.smartspaceinvaders.com/reset/password?token={token}'
                to = [form.cleaned_data['email']]
                send_mail(sub, mess, 'brhoome74@gmail.com', to)
                req.session['token'] = token
                req.session['email'] = form.cleaned_data['email']
                return render(req, 'success.html', {'password_reset':True})
            else:
                return render(req, 'pass_reset.html', {'send_reset_form':form,'error':'email is invalid'})

        except userInfo.DoesNotExist:
            return render(req, 'pass_reset.html', {'send_reset_form':form,'error':'email does not exist'})
    else:    
        form = send_reset_Form()
    return render(req, 'pass_reset.html',{'send_reset_form':form})

def reset_pass(req):
    if 'token' in req.session and req.session['token'] == req.GET.get('token'):
        if req.method == 'POST':
            form = change_pass_Form(req.POST)
            if form.is_valid() and form.cleaned_data['password1'] == form.cleaned_data['password2']:
                user = userInfo.objects.get(email=req.session['email'])
                user.password = form.cleaned_data['password1']
                user.save()
                del req.session['token']
                del req.session['email']
                return render(req, 'success.html', {'changed':True})
            else:
                return render(req, 'password_reset.html', {'change_pass_form':form, 'error':'password is invalid'})
            
        else:    
            form = change_pass_Form()
        return render(req, 'password_reset.html', {'change_pass_form':form})
    return redirect('home')    

def register_page(req):
    if 'authin' not in req.session:
        req.session['authin'] = False
        req.session['username'] = 'None'

    if req.method == 'POST':
        form = registerForm(req.POST)
    else:    
        form = registerForm()

    if req.method == 'POST':
        reg = r'(.+@hotmail\..{2,}|.+@yahoo\..{2,}|.+@gmail\..{2,}|.+@outlook\..{2,}|.+@student.ksu.edu.sa|.+@ksu.edu.sa|.+@KSU.EDU.SA)'
        form = registerForm(req.POST)
        if form.is_valid():
            if bool(re.match(reg, form.cleaned_data['email'])):
                if form.cleaned_data['password'] == form .cleaned_data['password_confirm']:
                    token = uuid.uuid4().hex
                    profile.objects.create(token=token, username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
                    

                    sub = 'smart space invaders verification'
                    mess = f'click the link to verify your email https://www.smartspaceinvaders.com/verify?token={token}'
                    to = [form.cleaned_data['email']]
                    send_mail(sub, mess, 'brhoome74@gmail.com', to)

                    return render(req, 'success.html', {'verify':True})
                else:
                    return render(req, 'register.html', {'register_form':form, 'auth': req.session['authin'], 'username':req.session['username'], 'error':'password and confirmed password not equal'})  
            else:
                return render(req, 'register.html', {'register_form':form, 'auth': req.session['authin'], 'username':req.session['username'], 'error':'email is not allowed please enter valid email'})    
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
