# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from re import sub
import sys
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
    except ValueError:
        print_exc(file=stderr)
        print("Oops!  That was no valid number.  Try again...")
        return text
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

