from typing import Any, Self

from django.forms import ClearableFileInput, SelectMultiple


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


class ArrayField(SelectMultiple):
    """
    Widget for rendering an array field.

    Requires:
    - Alpine.js for proper functionality
    - TailwindCSS for proper styling
    """

    template_name = "widgets/array_field.html"

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
