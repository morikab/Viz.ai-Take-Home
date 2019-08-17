from contextlib import contextmanager

from PIL import Image


class FaceImageMetadata(object):
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height


class FaceImage(object):
    def __init__(self, filepath):
        self.__filepath = filepath

        with Image.open(self.__filepath) as image:
            width, height = image.size
            self.__metadata = FaceImageMetadata(width, height)

    @contextmanager
    def image_stream(self):
        image = open(self.__filepath, 'r+b')
        yield image
        image.close()

    @property
    def metadata(self):
        return self.__metadata
