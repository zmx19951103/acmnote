# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^problems/$', views.problem_list_page, name='problem_list_page'),
    url(r'^problem/(?P<problem_id>\d+)/$', views.problem_page, name='problem_page'),
]