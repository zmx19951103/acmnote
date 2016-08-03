# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Problem, ProblemTag
from django.http import Http404
from .tables import ProblemTable
from note.models import ClassicNote
from authentication.models import MyUser
from django.db.models import Q, Count
# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound


def problem_list_page(request):
    """
    前台的问题列表
    """
    # 正常情况
    problem = Problem.objects.filter(visible=True)
    tag_text = request.GET.get("tag", None)
    tag = None
    if tag_text:
        try:
            tag = ProblemTag.objects.get(name=tag_text)
        except ProblemTag.DoesNotExist:
            raise Http404(u"标签不存在")
        problem = tag.problem_set.all().filter(visible=True)
    problems = ProblemTable(problem)
    tags = ProblemTag.objects.annotate(problem_number=Count("problem")).filter(problem_number__gt=0).order_by(
        "-problem_number")
    return render(request, 'problem/problem_list.html',
                  {'problem': problems, 'tags': tags, 'tag': tag})


def problem_page(request, problem_id):
    """
    前台题目详情页
    """
    user = request.user if request.user.is_authenticated() else None
    my_user = MyUser.objects.filter(user=user)
    try:
        problem = Problem.objects.get(id=problem_id, visible=True)
    except Problem.DoesNotExist:
        raise Http404(u"题目不存在")
    # status==0 表示尚未登陆只能查看
    # status==1 表示已经登陆且与该题没有relation，可以添加classic note
    # status==2 表示已经登陆且与该题有relation，可以修改classic note
    status = 0
    try:
        note = ClassicNote.objects.get(author=my_user, problem=problem)
    except ClassicNote.DoesNotExist:
        note = None
    if user:
        status = 2 if note else 1
    return render(request, 'problem/problem_page.html',
                  {'problem': problem, 'status': status, 'note': note})

