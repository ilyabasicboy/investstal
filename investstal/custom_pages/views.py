# -*- coding: utf-8 -*-
from ast import literal_eval

from django.http import JsonResponse
from django.template import loader
from django.views.generic import TemplateView

from ..custom_attachment.models import CustomAttachmentImage


class AbstractFilterView(TemplateView):
    template_name = None
    filter_by_page = True

    def get(self, request, *args, **kwargs):
        identifier = kwargs.get('page_id') or kwargs.get('page_ids')

        if self.filter_by_page:
            images = CustomAttachmentImage.objects.filter(page=identifier)
        else:
            id_list = literal_eval(identifier)
            images = CustomAttachmentImage.objects.filter(image_group__in=id_list).distinct()

        group = request.GET.get('group')
        if group:
            images = images.filter(image_group__in=[group])

        context = {
            'images': images,
        }

        if request.is_ajax():
            html = loader.render_to_string(self.template_name, context, request)
            response_data = {
                'html': html,
                'count': images.count(),
            }
            return JsonResponse(response_data)

        return self.render_to_response(context)


class FilterGroupedImages(AbstractFilterView):
    template_name = 'pages/parts/grouped_images_list.html'


class FilterGroupedImagesGallery(AbstractFilterView):
    template_name = 'pages/parts/grouped_images_list.html'
    filter_by_page = False
