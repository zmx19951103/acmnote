# -*- coding: utf-8 -*-
from .models import *
from table import Table
from table.utils import A
from table.columns import Column, LinkColumn
from util.mytables import MyLink
from util.mytables import MyDateTimeColumn


class GroupTable(Table):

    # id = LinkColumn(header=u'#',
    #                 links=[MyLink(field='id',
    #                               viewname='group_page',
    #                               args=(A('id'),)), ],
    #                 )
    id = Column(field='id', header=u'#',
                header_attrs={'width': '5%'})

    name = Column(field='name', header=u'名称',
                  header_attrs={'width': '15%'})

    join_method = Column(field='join_method', header=u'加入方式',
                         header_attrs={'width': '15%'})

    create_by = Column(field='create_user_name', header=u'创建者',
                       header_attrs={'width': '20%'})

    create_time = MyDateTimeColumn(field='create_time', header=u'创建时间',
                                   format="%Y年%m月%d日 %H:%I"
                                   )

    class Meta:
        model = Group
        search = True
        search_placeholder = 'search'
        pagination = True
        # ajax = True
