# -*- coding: utf-8 -*-
from .models import *
from table import Table
from table.utils import A
from table.columns import Column, LinkColumn, Link, DatetimeColumn


class ProblemTable(Table):
    id = Column(field='id', header=u'#', header_attrs={'width': '5%'})
    oj_all = Column(field='oj_all', header=u'OJ&ID', header_attrs={'width': '10%'})
    title = Column(field='title', header=u'标题', header_attrs={'width': '40%'})
    # tag = Column(field='get_tags_string', header=u'标签')
    difficulty_rank = Column(field='difficulty_rank', header=u'难度等级', header_attrs={'width': '13%'})
    difficulty_num = Column(field='difficulty_num', header=u'平均指数', header_attrs={'width': '13%'})
    action = LinkColumn(header=u'',
                        links=[Link(text=u'查看', viewname='problem_page', args=(A('id'),)), ],
                        header_attrs={'width': '7%'},
                        )

    class Meta:
        model = Problem
        search = True
        search_placeholder = 'search'
        pagination = True
