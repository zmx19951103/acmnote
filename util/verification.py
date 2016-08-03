# -*- coding: utf-8 -*-
# admin_type = 0 普通用户 能查看 能添加note
# admin_type = 1 普通管理员 能查看 能添加note 能管理tag，problem
# admin_type = 2 超级管理员 能进入django 后台


def user_check(user):
    if user.is_authenticated():
        return user.myuser.admin_type >= 0
    else:
        return False


def manager_check(user):
    if user.is_authenticated():
        return user.myuser.admin_type >= 1
    else:
        return False


def super_manger_check(user):
    if user.is_authenticated():
        return user.myuser.admin_type >= 2
    else:
        return False

