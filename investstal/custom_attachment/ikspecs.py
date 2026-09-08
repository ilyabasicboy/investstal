# -*- coding:utf-8 -*-
from imagekit.specs import ImageSpec
from .resizes import *


class Thumb(ImageSpec):
    processors = [ResizeThumb]


class Thumb300(ImageSpec):
    processors = [ResizeThumb300]


class Thumb500(ImageSpec):
    processors = [ResizeThumb500]


class Display(ImageSpec):
    processors = [ResizeDisplay]


class Img100x100(ImageSpec):
    # test spec
    quality = 50
    processors = [ResizeImg100x100]


class ImgAutox200(ImageSpec):
    # test spec
    processors = [ResizeImgAutox200]


class Img300x300(ImageSpec):
    # test spec
    processors = [ResizeImg300x300]
