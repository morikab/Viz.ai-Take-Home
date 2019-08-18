from contextlib import contextmanager

from PIL import Image


class FaceImage(object):
    def __init__(self, filepath):
        self.__filepath = filepath

        image_width, image_height = self.__get_image_size(filepath)

        self.__width = image_width
        self.__height = image_height

    @staticmethod
    def __get_image_size(filepath):
        with Image.open(filepath) as image:
            return image.size

    @contextmanager
    def image_stream(self):
        image = open(self.__filepath, 'r+b')
        yield image
        image.close()

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def filepath(self):
        return self.__filepath
