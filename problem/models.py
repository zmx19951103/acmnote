# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from .utils import *


class MyUser(models.Model):
    user = models.OneToOneField(User)
    real_name = models.CharField(max_length=32)
    permission = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    @property
    def all_name(self):
        return self.user.username + "(" + self.real_name + ")"


class ProblemTag(models.Model):
    # 短网址
    slug = models.CharField('网址', max_length=256, db_index=True)
    # 名字
    name = models.CharField('标签', max_length=30)
    # 简称
    abbreviation = models.CharField('简称', max_length=10, default="")
    # 简介
    intro = models.TextField('简介', default='')
    # 创建时间
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def get_absolute_url(self):
        return reverse('tag', args=(self.pk, self.slug))

    @property
    def get_rk(self):
        pt = ProblemTag.objects.get(id=self.id)
        p = pt.problem_set.all()
        n = len(p)
        return 200-150/(n+1)

    class Meta:
        db_table = "problem_tag"

    def __str__(self):
        return self.name


class Problem(models.Model):
    # 短网址
    slug = models.CharField('网址', max_length=256, db_index=True)
    # 所属OJ
    oj = models.CharField('所属OJ', max_length=30)
    # 所属OJ ID
    oj_id = models.CharField('OJ题号', max_length=30)
    # 标题
    title = models.CharField('标题', max_length=50)
    # 描述
    description = models.TextField('问题描述', max_length=30000)
    # hint
    hint = models.CharField('备注', blank=True, default="", max_length=256)
    # 创建时间
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    # 最后更新时间
    last_update_time = models.DateTimeField('最后更新时间', auto_now=True, blank=True, null=True)
    # 标签
    tags = models.ManyToManyField(ProblemTag)

    var = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('problem', args=(self.pk, self.slug))

    def get_notes(self):
        notes = Problem.objects.get(pk=self.pk).note_set.all()
        num = len(notes)
        self.var = num
        return notes

    def get_note_num(self):
        notes = Problem.objects.get(pk=self.pk).note_set.all()
        return len(notes)

    def init_var(self):
        self.var = self.get_note_num()

    def next_var(self):
        self.var -= 1
        return self.var

    @property
    def ac_user_num(self):
        relations = self.relation_set.all()
        cnt = 0
        for relation in relations:
            if relation.is_ac:
                cnt += 1
        return cnt

    @property
    def user_num(self):
        relations = self.relation_set.all()
        cnt = len(relations)
        return cnt

    @property
    def difficulty(self):
        relations = self.relation_set.all()
        total = 0.0
        cnt = 0.0
        for relation in relations:
            cnt += 1.0
            total += relation.difficulty
        if cnt == 0.0:
            # 返回一个dict
            return {'难度等级': '暂无', '难度系数': '暂无'}
        else:
            average = total/cnt
            if average < 4.0:
                return {'难度等级': u'简单', '难度系数': average}
            elif average > 7.0:
                return {'难度等级': u'困难', '难度系数': average}
            else:
                return {'难度等级': u'中等', '难度系数': average}

    @property
    def difficulty_rank(self):
        return self.difficulty['难度等级']

    @property
    def difficulty_num(self):
        return self.difficulty['难度系数']

    @property
    def get_all_tags(self):
        tg = Problem.objects.get(pk=self.pk).tags.all()
        res = ''
        for tag in tg:
            res += tag.abbreviation
            res += ','
        if res == '':
            res = u'暂无'
        else:
            l = len(res)
            res = res[:l-1]
        return res

    @property
    def get_tags(self):
        tg = Problem.objects.get(pk=self.pk).tags.all()
        return tg

    @property
    def get_tag_list(self):
        tg = Problem.objects.get(pk=self.pk).tags.all()
        return tg.name

    @property
    def oj_all(self):
        return self.oj+self.oj_id

    class Meta:
        db_table = "problem"
        ordering = ['oj', 'oj_id']

    def __str__(self):
        return self.oj_all+"("+self.title+")"


class Note(models.Model):
    problem = models.ForeignKey(Problem)
    # author = models.OneToOneField(MyUser)
    author = models.ForeignKey(MyUser)

    pub_time = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    content = models.TextField('记录', max_length=30000)

    @property
    def ac(self):
        relation = Relation.objects.filter(problem=self.problem, people=self.author)
        if relation:
            if relation.is_ac:
                return True
        return False

    @property
    def get_author_name(self):
        return self.author.all_name

    @property
    def get_problem_info(self):
        return self.problem.__str__()

    def get_relation(self):
        r = Relation.objects.get(problem=self.problem, people=self.author)
        return r

    @property
    def text(self):
        res = de_html(self.content)
        a = len(self.author.real_name)
        b = len(self.author.user.username)
        c = len(res)
        if a+b+c <= 60:
            return res
        else:
            return res[0: 60-a-b]+"..."

    @property
    def ordinal(self):
        return self.problem.oj_all+'-'+self.author.real_name

    class Meta:
        db_table = "note"
        ordering = ['-update_time']

    def __str__(self):
        return self.problem.oj_all+'-'+self.author.real_name


class Relation(models.Model):
    problem = models.ForeignKey(Problem)
    people = models.ForeignKey(MyUser)
    # 难度系数 1-10
    difficulty = models.IntegerField(blank=True, null=True)
    # AC 时间
    AC_time = models.DateTimeField(blank=True, null=True)

    @property
    def is_ac(self):
        if self.AC_time and self.AC_time < now():
            return True
        else:
            return False

    class Meta:
        db_table = "relation"
