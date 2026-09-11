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


class ResizeGalleryColumn(Resize):
    height = 600

    
class ResizeIntro(Resize):
    width = 2600


class ResizeSectionsCard(Resize):
    width = 1000


class ResizeProductCard(Resize):
    height = 400