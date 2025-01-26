from django import template
from django.db.models.manager import Manager
from django.forms import ImageField
from django.templatetags.static import static

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


@register.filter("imageurl")
def get_image_url(image: str | ImageField) -> str:
    """
    Gets image URL to display or a placeholder if no image is available.

    :param image: Image path (obtained i.e. by using `.values()`) or an ImageField instance
    :return: URL of an image suitable to use in the HTML `src=` attribute
    """
    if not image:
        return static("img/image-placeholder.png")

    image_path = image if isinstance(image, str) else image.name
    return EntityBase.image.field.storage.url(image_path)
