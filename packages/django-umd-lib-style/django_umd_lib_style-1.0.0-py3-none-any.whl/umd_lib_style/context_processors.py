import importlib.metadata
from importlib import import_module
from typing import Any

from django.conf import settings
from django.http import HttpRequest


def get_links(request: HttpRequest, key: str) -> dict:
    links = getattr(settings, key, {})

    if isinstance(links, str):
        # this is a fully-qualified name to a function to run to get the links
        # this allows applications to customize the links on a per-request basis
        module_name, function_name = links.rsplit('.', 1)
        module = import_module(module_name)
        function = getattr(module, function_name)
        links = function(request)

    return links


def app_info(request: HttpRequest) -> dict[str, Any]:
    package_name = getattr(settings, 'PROJECT_PACKAGE_NAME', None)

    return {
        'application_name': getattr(settings, 'APPLICATION_NAME', 'App'),
        'application_version': importlib.metadata.version(package_name) if package_name is not None else '',
        'navigation_links': get_links(request, 'NAVIGATION_LINKS'),
        'footer_links': get_links(request, 'FOOTER_LINKS'),
    }
