from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login as auth_login
from acmnote2.settings import super_manager_code, manager_code

from .models import MyUser

from .forms import RegisterForm, LoginForm


# Create your views here.
def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    if request.method == 'POST':
        form = RegisterForm(request.POST, request=request)
        if form.is_valid():
            user = form.save(commit=False)
            real_name = request.POST.get('real_name')
            admin_type = 0
            if 'code' in request.POST:
                code = request.POST['code']
                if code == super_manager_code:
                    admin_type = 2
                    user.is_staff = True
                elif code == manager_code:
                    admin_type = 1
            user.save()
            my_user = MyUser(user=user, real_name=real_name, admin_type=admin_type)
            my_user.save()
            # return redirect('authentication.views.login', permanent=True)
            form = LoginForm()
            return render(request, 'authentication/login.html', {'form': form, 'info': '注册成功，请登陆！'})
        else:
            return render(request, 'authentication/signup.html', {'form': form})

    else:
        form = RegisterForm()
        return render(request, 'authentication/signup.html', {'form': form})


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        next_page = request.GET.get('next', reverse('homepage'))

        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(next_page)
        else:
            return render(request, 'authentication/login.html', {'form': form, 'next': next_page})
    else:
        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))

