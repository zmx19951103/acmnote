# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Announcement

from util.shortcuts import error_page


def announcement_page(request, announcement_id):
    """
    公告的详情页面
    """
    try:
        announcement = Announcement.objects.get(id=announcement_id, visible=True)
    except Announcement.DoesNotExist:
        return error_page(request, u"公告不存在")
    return render(request, "announcement/announcement.html", {"announcement": announcement})
