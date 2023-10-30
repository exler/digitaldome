from typing import Any, Self
from urllib.parse import urlparse

from django import template
from django.db.models import Model
from django.forms import BoundField
from django.http import HttpRequest
from django.template.defaultfilters import stringfilter
from django.utils.safestring import SafeString

from digitaldome.utils.url import get_full_url

register = template.Library()


class MissingTemplateWidget(Exception):
    def __init__(
        self: Self,
        msg: str = "Cannot add class name to a non-widget object",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(msg, *args, **kwargs)


@register.filter("verbosename")
def verbose_name(value: Model) -> str:
    return value._meta.verbose_name


@register.filter("addclass")
def add_class(value: BoundField, arg: str) -> SafeString:
    try:
        return value.as_widget(attrs={"class": arg})
    except AttributeError:
        raise MissingTemplateWidget


@register.filter("fieldlabel")
def field_label(value: Model, arg: str) -> str:
    return value._meta.get_field(arg).verbose_name


@register.filter("toint")
def to_int(value: str) -> int:
    return int(value)


@register.filter("baseurl")
@stringfilter
def base_url(value: str) -> str:
    return urlparse(value).netloc


@register.simple_tag
def full_url(path: str) -> str:
    return get_full_url(path)


@register.simple_tag(takes_context=True)
def merge_query_params(context: dict, **new_params: str) -> str:
    request: HttpRequest = context["request"]
    params = request.GET.copy()
    for key, value in new_params.items():
        params[key] = value
    return f"?{params.urlencode()}"


@register.filter("getattr")
def get_attr(obj: object, attr: str) -> object:
    return getattr(obj, attr)
