from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponseNotFound
from django.template import loader
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .models import ParameterValue, Root


class FilterProductViewFp(TemplateView):
    """ Фильтр новинок на главной"""

    template_name = 'catalog/parts/product_slider_cards.html'

    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')

        object = Root.objects.first()
        products = object.get_products().order_by('-id')

        if category:
            products = products.filter(category=category)

        context = {
            'product_list': products,
        }
        if request.is_ajax():
            html = loader.render_to_string(self.template_name, context, request)
            response_data = {
                'html': html,
                'products_count': products.count(),
            }
            return JsonResponse(response_data)
        return self.render_to_response(context)


def change_parameters(request):
    parameter_group = request.GET.get('parameter_group')
    if parameter_group:
        parameters = ParameterValue.objects.filter(parameter_group=parameter_group).order_by('value')
        context = {
            'parameters': parameters
        }
        return render(request, 'admin/custom_catalog/parameterinline/parameters.html', context)
    raise PermissionDenied
