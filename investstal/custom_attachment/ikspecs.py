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


class Intro(ImageSpec):
    processors = [ResizeIntro]
