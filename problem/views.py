# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from problem.models import Problem, ProblemTag, Note, MyUser
from problem.utils import permission_check, manage_check
from acmnote.settings import register_code, manager_code

from .forms import *

from django.utils.timezone import now
from datetime import datetime
from django.shortcuts import redirect
from .tables import *


def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'index.html', content)


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username',)
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=request.POST.get('email', ''))
                new_user.is_staff = False
                new_user.is_superuser = False
                new_user.save()
                code = request.POST.get('code', '')
                permission = 0
                if code == manager_code:
                    permission = 2
                    new_user.is_staff = True
                elif code == register_code:
                    permission = 1
                new_my_user = MyUser(user=new_user, real_name=request.POST.get('real_name', ''),
                                     permission=permission)
                new_my_user.save()
                state = 'success'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'signup.html', content)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }
    return render(request, 'set_password.html', content)


@user_passes_test(manage_check, login_url='/login/')
def add_tag(request):
    if request.method == "POST":
        form = ProblemTagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.create_time = now()
            tag.slug = tag.abbreviation.lower()
            tag.save()
            # return HttpResponseRedirect(reverse('homepage'))
            return redirect('problem.views.index')
        else:
            return render(request, 'add_tag.html', {'form': form})
    else:
        form = ProblemTagForm()
        return render(request, 'add_tag.html', {'form': form})


@user_passes_test(permission_check, login_url='/login/')
def add_note(request, problem_pk):
    user = request.user
    problem = Problem.objects.get(pk=problem_pk)
    my_user = MyUser.objects.get(user=user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = my_user
            note.problem = problem
            note.pub_time = now()
            note.save()
            num = request.POST.get('difficulty', False)
            relation = Relation(problem=problem, people=my_user, difficulty=num)
            if 'ac_time' in request.POST:
                ac_time = request.POST['ac_time']
                if ac_time:
                    ac_time = datetime.strptime(ac_time, "%Y/%m/%d %H:%M")
                    relation.AC_time = ac_time
            relation.save()
            # 实现方式并不优雅=  =先就这样啊啊啊
            # 两种方式都行
            return redirect('problem.views.view_note', pk=note.pk, permanent=True)
            # content = {
            #     'user': user,
            #     'active_menu': 'view_note',
            #     'note': note,
            #     'editable': True,
            #     # 'pk': note.pk
            # }
            # return render(request, 'view_note.html', content)
        else:
            content = {
                'problem': problem,
                'my_user': my_user,
                'form': form
            }
            return render(request, 'add_note.html', content)
    else:
        form = NoteForm()
        content = {
            'problem': problem,
            'my_user': my_user,
            'form': form
        }
        return render(request, 'add_note.html', content)


@user_passes_test(manage_check)
def add_problem(request):
    # wait...
    return render(request)


def view_problem_list(request):
    # waiting...
    user = request.user if request.user.is_authenticated() else None
    problem = ProblemTable()
    # problem.action2.visible = False
    # if user:
    #     if permission_check(user):
    #         problem.action2.visible = False
    content = {
        'user': user,
        'active_menu': 'view_problem',
        'problem': problem
    }
    return render(request, 'view_problem_list.html', content)


def view_problem(request, pk):
    user = request.user if request.user.is_authenticated() else None
    my_user = MyUser.objects.filter(user=user)
    problem = Problem.objects.get(pk=pk)
    # status==0 表示尚未登陆只能查看
    # status==1 表示已经登陆且与该题没有relation，可以添加
    # status==2 表示已经登陆且与该题有relation，可以修改
    status = 0
    relation = Relation.objects.filter(people=my_user, problem=problem)
    if user:
        status = 2 if relation else 1
    content = {
        'user': user,
        'active_menu': 'view_problem',
        'problem': problem,
        'status': status,
    }
    return render(request, 'view_problem.html', content)


def view_note_list(request):
    user = request.user if request.user.is_authenticated() else None
    note = NoteTable()
    content = {
        'user': user,
        'active_menu': 'view_note',
        'note': note
    }
    return render(request, 'view_note_list.html', content)


def view_note(request, pk):
    user = request.user if request.user.is_authenticated() else None
    note = Note.objects.get(pk=pk)
    editable = False
    if user:
        if user.pk == note.author.pk:
            editable = True
    content = {
        'user': user,
        'active_menu': 'view_note',
        'note': note,
        'editable': editable,
    }
    return render(request, 'view_note.html', content)

