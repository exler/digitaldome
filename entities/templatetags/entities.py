from django import template
from django.db.models.manager import Manager

from entities.models import EntityBase

register = template.Library()


@register.filter("detailfieldhtml")
def get_detail_field_html(obj: EntityBase, field_name: str) -> str:
    if hasattr(obj, f"get_{field_name}_display"):
        return getattr(obj, f"get_{field_name}_display")()

    field_value = getattr(obj, field_name)
    if isinstance(field_value, list):
        return ", ".join(field_value)
    elif isinstance(field_value, Manager):
        return ", ".join(str(obj) for obj in field_value.all())
    return str(field_value)
