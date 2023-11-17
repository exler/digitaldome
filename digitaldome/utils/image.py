from io import BytesIO

from django.core.files.base import ContentFile, File
from PIL import Image


def resize_and_crop_image(image: File, width: int, height: int) -> File:
    """
    Resize image while maintaining aspect ratio. Crop image if necessary.
    """

    img = Image.open(image)
    img_format = img.format

    img_width, img_height = img.size

    width_scale = width / img_width
    height_scale = height / img_height

    if width_scale > height_scale:
        img = img.resize((int(img_width * height_scale), height))
    else:
        img = img.resize((width, int(img_height * width_scale)))

    img_width, img_height = img.size
    left = (img_width - width) / 2
    top = (img_height - height) / 2
    right = (img_width + width) / 2
    bottom = (img_height + height) / 2

    img = img.crop((left, top, right, bottom))

    img_io = BytesIO()
    img.save(img_io, format=img_format)

    return ContentFile(img_io.getvalue(), name=image.name)
