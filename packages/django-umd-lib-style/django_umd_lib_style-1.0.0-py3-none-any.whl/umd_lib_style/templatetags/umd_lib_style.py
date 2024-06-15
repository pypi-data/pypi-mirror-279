from django import template
from django.conf import settings
from django.template.defaultfilters import safe

register = template.Library()

ENVIRONMENT_LABELS = {
    'development': 'Local Environment',
    'test': 'Test Environment',
    'qa': 'QA Environment',
}


@register.inclusion_tag('umd_lib_style/header.html', takes_context=True)
def umd_header(context, application_name: str = 'App'):
    context['application_name'] = application_name
    return context


@register.simple_tag()
def environment_banner():
    environment = getattr(settings, 'ENVIRONMENT', None)
    if environment is None:
        return ''

    label = ENVIRONMENT_LABELS.get(environment, None)
    if label is None:
        return ''

    return safe(f'<div class="{environment} environment-banner">{label}</div>')
