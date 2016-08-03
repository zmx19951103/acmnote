# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class MyUser(models.Model):
    # 对应到一个User
    user = models.OneToOneField(User)
    # 真实姓名
    real_name = models.CharField(max_length=30, blank=True, null=True)
    # 用户注册时间
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    # 0代表不是管理员 1是普通管理员 2是超级管理员
    admin_type = models.IntegerField(default=0)
    # 是否禁用用户
    is_forbidden = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @property
    def all_name(self):
        return self.user.username + "(" + self.real_name + ")"

    class Meta:
        db_table = 'user'


