from django.shortcuts import render
from feedback.utils import get_feedback_form
from feedback.settings import PREFIX_KEY_FIELDS


def ajax_reset_form(request):
    form_key = request.GET.get('form_key')
    form = get_feedback_form(form_key)
    if PREFIX_KEY_FIELDS:
        form.prefix = form_key
    templates = ['feedback/%s/feedback.html' % form_key, 'feedback/feedback.html']
    return render(request, templates, {'form': form})
