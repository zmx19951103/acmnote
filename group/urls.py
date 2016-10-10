# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^note/(?P<note_id>\d+)/$', views.note_page, name='note_page'),

    url(r'^groups/$', views.group_list_page, name='group_list_page'),
]
