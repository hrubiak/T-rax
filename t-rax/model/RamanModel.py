# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from .BaseModel import SingleSpectrumModel


class RamanModel(SingleSpectrumModel, object):
    def __init__(self):
        super(RamanModel, self).__init__()