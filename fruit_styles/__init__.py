"""
The nbconvert exporter for the Avocado template.
"""
import os
import base64

from nbconvert.exporters import SlidesExporter


class AvocadoExporter(SlidesExporter):
    """
    A custom exporter that points to the Avocado Reveal slides
    template.
    """
    custom_template_name = 'avocado'
    pkg_dir = os.path.dirname(__file__)
    template_dir = os.path.join(pkg_dir, custom_template_name)

    @property
    def extra_template_basedirs(self):
        return super()._default_extra_template_basedirs() + [self.template_dir]

    def _template_name_default(self):
        return os.path.join(self.pkg_dir, self.custom_template_name)

    def _init_resources(self, resources):
        resources = super()._init_resources(resources)
        resources['avocado-img'] = encode_image(
            os.path.join(self.template_dir, 'avocado.jpg')
        )
        return resources


def encode_image(image_path):
    """
    Encodes an image as a base64 string.
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode()
