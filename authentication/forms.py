# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import  *
from util.captcha import Captcha

from .models import *


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RegisterForm, self).__init__(*args, **kwargs)

    # 设置邮箱为必须
    email = forms.EmailField(required=True)
    # 真实姓名
    real_name = forms.CharField(label='真实姓名', max_length=30, required=True)

    captcha = forms.CharField(label='验证码')
    # 邀请码
    code = forms.CharField(label='邀请码', required=False, initial='', help_text='邀请码可为空')

    def clean_captcha(self):
        captcha = Captcha(self.request)
        data = self.cleaned_data["captcha"]
        if not captcha.check(data):
            msg = "验证码错误！"
            self.errors['captcha'] = self.error_class([msg])
        return data

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                msg = "你输入的账号和密码不匹配，请重试"
                self.errors['password'] = self.error_class([msg])
                self.errors['username'] = self.error_class([" "])
                # raise forms.ValidationError(
                #     self.error_messages['invalid_login'],
                #     code='invalid_login',
                #     params={'username': self.username_field.verbose_name},
                # )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active or user.myuser.is_forbidden:
            msg = "用户已被禁止使用，请联系管理员"
            self.errors['password'] = self.error_class([msg])
            self.errors['username'] = self.error_class([" "])
            # raise forms.ValidationError(
            #     "This account is inactive or is forbidden.",
            #     code='inactive_forbidden',
            # )
        permission = user.myuser.admin_type
        if permission < 0 or permission > 2:
            msg = "非法的用户类型，请联系管理员"
            self.errors['password'] = self.error_class([msg])
            self.errors['username'] = self.error_class([" "])
            # raise forms.ValidationError(
            #     "Sorry, This account's type isn't welcome here.",
            #     code='no_that_type',
            # )

