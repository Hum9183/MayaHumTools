# -*- coding: utf-8 -*-
EMPTY = ''


def decode(string):
    try:
        return string.decode('utf-8')
    except UnicodeEncodeError:
        return string
    except AttributeError:
        return string
