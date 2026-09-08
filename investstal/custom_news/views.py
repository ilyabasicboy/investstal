from django.shortcuts import render, get_object_or_404
from .models import NewsRoot


def news_root(request):
    template = 'easy_news/root.html'
    context = {
        'object': get_object_or_404(NewsRoot),
    }
    return render(request, template, context)