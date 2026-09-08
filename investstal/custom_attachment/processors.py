
# -*- coding: utf-8 -*-
from . import resizes


def filebrowser_processor(img, verbose_name):

    """ Применение файлбраузером процессоров из attachments """

    ResizeClass = getattr(resizes, 'Resize' + verbose_name)
    img, fmt = ResizeClass.process(img, img.format, None)
    return img
