# -*- coding: utf-8 -*-
# permission = 0 普通用户 只能查看 不能添加
# permission = 1 授权用户 能查看 能添加note 不能管理
# permission = 2 管理员
from html.parser import  HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc


class DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attr):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attr):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def de_html(text):
    try:
        parser = DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text


def permission_check(user):
    if user.is_authenticated():
        return user.myuser.permission > 0
    else:
        return False


def manage_check(user):
    if user.is_authenticated():
        return user.myuser.permission > 1
    else:
        return False

