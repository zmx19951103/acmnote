from django.db import models

# Create your models here.
from authentication.models import MyUser
from problem.models import Problem
from util.dehtml import de_html
from django.utils.timezone import now


class AbstractNote(models.Model):
    # 对应问题
    problem = models.ForeignKey(Problem)
    # 对应发表者
    author = models.ForeignKey(MyUser)
    # 发表时间
    pub_time = models.DateTimeField('发表时间', auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)
    # 内容
    content = models.TextField('记录', max_length=30000)

    @property
    def get_author_name(self):
        return self.author.all_name

    @property
    def get_problem_info(self):
        return self.problem.__str__()

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

    def __str__(self):
        return self.ordinal

    class Meta:
        db_table = "note"
        ordering = ['-update_time']
        abstract = True


# 每个用户每个题只能有一个ClassicNote
class ClassicNote(AbstractNote):
    # 难度系数 1-10
    ac_time = models.DateTimeField(blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)

    @property
    def ac(self):
        if self.ac_time and self.ac_time < now():
            return True
        else:
            return False
