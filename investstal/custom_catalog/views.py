from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponseNotFound
from django.template import loader
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from catalog.utils import get_sorted_content_objects
from .models import (
    Category,
    ParameterValue,
    Product,
    Root,
    Section,
    ParameterGroup
)
from investstal.custom_attachment.utils import attach_images_queryset


class FilterProductView(TemplateView):
    """Фильтр каталога."""

    template_name = 'catalog/parts/product_list.html'

    def get(self, request, *args, **kwargs):
        ct_id = request.GET.get('ct')
        obj_id = request.GET.get('obj')
        sort_dir = request.GET.get('dir')
        category = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        paginate_by = 24

        if ct_id and obj_id:
            object = ContentType.objects.filter(id=ct_id).first()
            if object:
                object = object.get_all_objects_for_this_type().filter(id=obj_id).first()
        else:
            object = Root.objects.first()

        if not object:
            products = Product.objects.none()
        else:
            products = object.get_products()

        context = {
            'object': object,
        }

        if min_price or max_price:
            try:
                if min_price:
                    products = products.filter(price__gte=int(min_price))
                if max_price:
                    products = products.filter(price__lte=int(max_price))
            except (TypeError, ValueError):
                pass

        if category:
            try:
                content_type, category_id = category.split('_')
                if content_type == 'category':
                    products = products.filter(category=category_id)
                    chosen_category = Category.objects.get(id=category_id)
                elif content_type == 'section':
                    chosen_category = Section.objects.get(id=category_id)
                    products = products.filter(id__in=chosen_category.get_products().values_list('id', flat=True))
                else:
                    chosen_category = None

                if chosen_category:
                    context['chosen_category'] = chosen_category
                    paginate_by = 23
            except:
                pass

        if sort_dir == 'asc':
            products = products.order_by('price')
        elif sort_dir == 'desc':
            products = products.order_by('-price')
        elif sort_dir == 'popular':
            products = get_sorted_content_objects(products)
        else:
            products = products.order_by('-id')

        try:
            products_count = products.count()
        except:
            try:
                products_count = len(products)
            except:
                products_count = 0

        context['products'] = products
        context['paginate_by'] = paginate_by

        if request.is_ajax():
            html = loader.render_to_string(self.template_name, context, request)
            return JsonResponse({
                'html': html,
                'count': products_count,
                'min_price': min_price,
                'max_price': max_price,
                'dir': sort_dir,
            })
        return self.render_to_response(context)


class FilterProductViewFp(TemplateView):
    """ Фильтр новинок на главной"""

    template_name = 'catalog/parts/product_slider_cards.html'

    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')

        object = Root.objects.first()
        products = object.get_products().order_by('-id')

        if category:
            products = products.filter(category=category)

        products = attach_images_queryset(products)

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


def parameter_popup(request, obj_id):

    parameter = ParameterValue.objects.filter(id=obj_id).first()

    if parameter:
        try:
            image_id = int(request.GET.get('image_id'))
        except:
            image_id = None

        html = loader.render_to_string(
            'catalog/parts/parameter_popup.html',
            {
                'parameter': parameter,
                'image_id': image_id,
            },
            request
        )
        response_data = {
            'html': html
        }

        return JsonResponse(response_data)
    return HttpResponseNotFound
