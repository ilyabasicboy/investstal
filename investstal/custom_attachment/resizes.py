# -*- coding:utf-8 -*-
from imagekit.processors import Resize


class Resize80x56(Resize):
    width = 80
    height = 56
    crop = True


class ResizeThumb(Resize):
    width = 172
    height = 172


class ResizeThumb300(Resize):
    height = 300


class ResizeThumb500(Resize):
    height = 500


class ResizeDisplay(Resize):
    width = 1200
    height = 900


class ResizeImg300x300(Resize):
    # test resize
    width = 300
    height = 300
    crop = True


class ResizeImgAutox200(Resize):
    # test resize
    height = 200


class ResizeImg100x100(Resize):
    # test resize
    width = 100
    height = 100
