

class DetectedFace(object):
    def __init__(self, face_metadata, face_image):
        self.__face_metadata = face_metadata
        self.__face_image = face_image

    @property
    def metadata(self):
        return self.__face_metadata

    @property
    def face_image(self):
        return self.__face_image
