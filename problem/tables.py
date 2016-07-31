# -*- coding: utf-8 -*-
from .models import *
from table import Table
from table.utils import A
from table.columns import Column, LinkColumn, Link, DatetimeColumn


class ProblemTable(Table):
    id = Column(field='pk', header=u' ', attrs={'class': 'custom'}, header_attrs={'width': '10%'})
    oj_all = Column(field='oj_all', header=u'OJ&ID')
    title = Column(field='title', header=u'title')
    tag = Column(field='get_all_tags', header=u'Tags',)
    difficulty_rank = Column(field='difficulty_rank', header=u'rank',)
    action = LinkColumn(header=u'action',
                        links=[Link(text=u'View', viewname='view_problem', args=(A('id'),)), ],
                        header_attrs={'width': '10%'},
                        )
    # action2 = LinkColumn(header=u'action',
    # links=[Link(text=u'AddNote', viewname='add_note', args=(A('id'),)),],
    #                      header_attrs={'width': '10%'},
    #                      )

    class Meta:
        model = Problem
        search = True
        pagination = True


class NoteTable(Table):
    id = Column(field='pk', header=u' ', attrs={'class': 'custom'}, header_attrs={'width': '10%'})
    problem_info = Column(field='get_problem_info', header=u'problem')
    people = Column(field='get_author_name', header=u'author')

    update_time = DatetimeColumn(field='update_time', header=u'update time')
    pub_time = DatetimeColumn(field='pub_time', header=u'pub time')

    class Meta:
        model = Note
        search = True
        pagination = True
