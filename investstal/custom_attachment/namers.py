# -*- coding: utf-8 -*-
from django.conf import settings


class VersionNamer(object):

    """ Кастомизован для именование ресайзов файлбраузера идентично с attachments """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_version_name(self):
        return self.file_object.filename_root + "-" + self.version_suffix + self.extension

    def get_original_name(self):
        tmp = self.file_object.filename_root.split("-")
        if tmp[len(tmp) - 1] in settings.FILEBROWSER_ADMIN_VERSIONS:
            return "%s%s" % (
                self.file_object.filename_root.replace("-%s" % tmp[len(tmp) - 1], ""),
                self.file_object.extension)

