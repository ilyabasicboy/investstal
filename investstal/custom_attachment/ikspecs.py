# -*- coding:utf-8 -*-
from imagekit.specs import ImageSpec
from .resizes import *


class CustomImageSpec(ImageSpec):

    """ Added fix for png images """

    @classmethod
    def process(cls, image, obj):
        fmt = image.format
        img = image.copy()
        if img.mode != 'RGBA' and img.mode != 'RGB' and fmt != 'JPEG':
            img = img.convert('RGBA')
        for proc in cls.processors:
            img, fmt = proc.process(img, fmt, obj)
        img.format = fmt
        return img, fmt


class Thumb(ImageSpec):
    processors = [ResizeThumb]


class Thumb300(ImageSpec):
    processors = [ResizeThumb300]


class Thumb500(ImageSpec):
    processors = [ResizeThumb500]


class Display(ImageSpec):
    processors = [ResizeDisplay]


class GalleryColumn(ImageSpec):
    processors = [ResizeGalleryColumn]


class WatermarkPicture(ImageSpec):
    processors = [ResizeDisplay]


class Intro(ImageSpec):
    processors = [ResizeIntro]


class SectionsCard(ImageSpec):
    processors = [ResizeSectionsCard]


class ProductCard(ImageSpec):
    quality = 100
    processors = [ResizeProductCard]


class ProductSlider(CustomImageSpec):
    quality = 100
    processors = [ResizeProductSlider]


class ProductThumb(CustomImageSpec):
    quality = 100
    processors = [ResizeProductThumb]


class FinishCard(CustomImageSpec):
    quality = 100
    processors = [ResizeFinishCard]
