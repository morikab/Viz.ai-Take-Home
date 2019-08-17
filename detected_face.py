

class DetectedFace(object):
    def __init__(self, face_metadata, image_metadata):
        self.__face_metadata = face_metadata
        self.__face_image_ratio = self.__calculate_face_image_ratio(face_metadata, image_metadata)

    @staticmethod
    def __calculate_face_image_ratio(face_metadata, image_metadata):
        image_area = image_metadata.width*image_metadata.height
        face_area = 0  # TODO - FIXME
        return face_area/image_area

    @property
    def metadata(self):
        return self.__face_metadata

    @property
    def face_image_ratio(self):
        return self.__face_image_ratio
