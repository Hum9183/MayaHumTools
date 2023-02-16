# -*- coding: utf-8 -*-
from .reassignment_error import ReassignmentError


class ReadonlyAttr:
    def __setattr__(self, name, value): # override
        if name in self.__dict__.keys():
            raise ReassignmentError(name, value, self.__class__.__name__)
        self.__dict__[name] = value