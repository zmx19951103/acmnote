# -*- coding: utf-8 -*-
from .models import *
from table import Table
from table.utils import A
from table.columns import Column, LinkColumn, Link, DatetimeColumn


class ClassicNoteTable(Table):

    id = Column(field='id', header=u'#',
                header_attrs={'width': '5%'})
    user = Column(field='get_author_name', header=u'用户',
                  header_attrs={'width': '20%'})
    problem_info = Column(field='get_problem_info', header=u'题目信息',
                          header_attrs={'width': '20%'})
    pub_time = DatetimeColumn(field='pub_time', header=u'发表时间',
                              format="%Y年%m月%d日 %H:%I"
                              )
    update_time = DatetimeColumn(field='update_time', header=u'最后更新时间',
                                 format="%Y年%m月%d日 %H:%I"
                                 )

    action = LinkColumn(header=u'',
                        links=[Link(text=u'查看', viewname='note_page',
                                    args=(A('id'),)), ],
                        header_attrs={'width': '7%'},
                        )

    class Meta:
        model = ClassicNote
        search = True
        search_placeholder = 'search'
        pagination = True
