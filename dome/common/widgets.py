from typing import Any, Self

from django.forms import ClearableFileInput, MultiWidget, NumberInput, SelectMultiple
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict


class ClearableFileInputWithImagePreview(ClearableFileInput):
    """
    Widget for rendering a clearable file input with a preview of the image.

    Requires:
    - Alpine.js for proper functionality
    - TailwindCSS for proper styling
    """

    template_name = "widgets/clearable_file_input_with_image_preview.html"

    def __init__(self: Self, attrs: dict | None = None) -> None:
        attrs = attrs or {}
        if not all(key in attrs for key in ("width", "height", "placeholder")):
            raise ValueError("All of 'width', 'height' and 'placeholder' must be provided.")
        super().__init__(attrs)


class TagWidget(SelectMultiple):
    """
    Widget for rendering an array-like field.

    Requires:
    - Alpine.js for proper functionality
    - TailwindCSS for proper styling
    """

    template_name = "widgets/tag_widget.html"

    def format_value(self: Self, value: Any) -> list[str]:
        if not value:
            return []

        if isinstance(value, str):
            return value.split(",")

        return [str(v) for v in value]


class ManyToManyWithTextInput(SelectMultiple):
    """
    Widget for rendering a many to many field with text input (for creating new entities).

    Allows for free text input, selecting from a pre-defined list of choices
    and searching through the choices.

    Requires:
    - Alpine.js for proper functionality
    - TailwindCSS for proper styling
    """

    template_name = "widgets/many_to_many_with_text_input.html"


class TimeWidget(MultiWidget):
    """
    Widget for rendering a "length" field. It consists of two number fields:
    one for hours and one for minutes. Internally, the value is stored as minutes.
    """

    template_name = "widgets/time_widget.html"

    def __init__(self: Self, attrs: dict | None = None) -> None:
        widgets = [
            NumberInput(attrs=attrs),  # Hours
            NumberInput(attrs=attrs),  # Minutes
        ]
        super().__init__(widgets, attrs)

    def decompress(self: Self, value: int) -> list[int | None]:
        if value:
            hours = value // 60  # Convert total minutes to hours
            minutes = value % 60  # Get remaining minutes
            return [hours, minutes]
        return [None, None]

    def value_from_datadict(self: Self, data: QueryDict, files: MultiValueDict, name: str) -> int | None:
        hours, minutes = [
            widget.value_from_datadict(data, files, name + "_%s" % i) for i, widget in enumerate(self.widgets)
        ]
        try:
            # Convert hours and minutes to total minutes
            total_minutes = int(hours) * 60 + int(minutes)
        except ValueError:
            return None
        return total_minutes
