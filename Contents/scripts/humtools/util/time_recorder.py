# -*- coding: utf-8 -*-
import functools
import time

from .log import Log


class TimeRecorder:
    @staticmethod
    def wraps(function):
        """処理時間を記録するデコレータ"""
        @functools.wraps(function)
        def wrapper(*args, **keywords):
            timeRecorder = TimeRecorder()
            timeRecorder.start()
            returnValue = function(*args, **keywords)
            timeRecorder.end()
            Log.log(u"実行時間: {}秒".format(timeRecorder.getDeltaTime()))
            return returnValue
        return wrapper

    def __init__(self):
        self.__startTime = 0
        self.__endTime = 0

    def start(self):
        self.__startTime = time.time()

    def end(self):
        self.__endTime = time.time()

    def getDeltaTime(self):
        return self.__endTime - self.__startTime
