from collections import namedtuple

from azure.cognitiveservices.vision.face.models import APIErrorException

from vizapp.face.face_image import FaceImage
from vizapp.request_exceptions import InvalidRequestDataFormat, MissingRequestDataKey, EmptyRequestData

DetectedFaceImageTuple = namedtuple('DetectedFaceImageTuple', 'face, face_image')


class MostCommonFaceError(Exception):
    def __init__(self, message, exception=None):
        super().__init__(message)
        self.__exception = exception

    def cause(self):
        if self.__exception is not None:
            return str(self.__exception)
        return None


class MostCommonFace(object):
    @staticmethod
    def __detect_faces(face_client, face_images):
        total_detected_faces = {}

        for face_image in face_images:
            with face_image.image_stream() as image_stream:
                detected_faces = face_client.face.detect_with_stream(image_stream, return_face_id=True,
                                                                     return_face_landmarks=True)
                for face in detected_faces:
                    total_detected_faces[face.face_id] = DetectedFaceImageTuple(face=face, face_image=face_image)

        return total_detected_faces

    @staticmethod
    def __calculate_face_image_ratio(face_metadata, face_image):
        image_area = face_image.width*face_image.height
        face_area = face_metadata.face_rectangle.width*face_metadata.face_rectangle.height
        return face_area/image_area

    @staticmethod
    def __find_best_face(group, detected_faces):
        group_detected_faces = [detected_faces[face_id] for face_id in group]

        return max(group_detected_faces, key=lambda detected_face: MostCommonFace.__calculate_face_image_ratio(
            detected_face.face, detected_face.face_image))

    @staticmethod
    def __format_result(detected_face):
        return {"image_filepath": detected_face.face_image.filepath,
                "face_id": detected_face.face.face_id,
                "face_rectangle": {
                    "top": detected_face.face.face_rectangle.top,
                    "left": detected_face.face.face_rectangle.left,
                    "width": detected_face.face.face_rectangle.width,
                    "height": detected_face.face.face_rectangle.height }
                }

    @staticmethod
    def __format_empty_result():
        return {"image_filepath": None,
                "face_id": None,
                "face_rectangle": None}

    @staticmethod
    def __get_most_common_face_ids(face_client, detected_faces):
        if len(detected_faces) == 1:
            # If there's only one face return its key
            return detected_faces.keys()

        group_result = face_client.face.group(detected_faces.keys())

        if not group_result.groups:
            # All faces are equally common.
            common_group = group_result.messy_group
        else:
            common_group = max(group_result.groups, key=len)

        return common_group

    @staticmethod
    def __get_image_filepaths(request_json_data):
        request_images_key = "images"

        if request_images_key not in request_json_data:
            raise MissingRequestDataKey(request_images_key)

        image_filepaths = request_json_data[request_images_key]

        if not isinstance(image_filepaths, list):
            raise InvalidRequestDataFormat(request_images_key, "list")

        if not image_filepaths:
            raise EmptyRequestData(request_images_key)

        return image_filepaths

    @staticmethod
    def most_common_face_from_image_filepaths(face_client, request_json_data):
        image_filepaths = MostCommonFace.__get_image_filepaths(request_json_data)
        try:
            face_images = [FaceImage(filepath) for filepath in image_filepaths]
        except IOError as e:
            raise MostCommonFaceError("Failed to load image file", e)

        try:
            detected_faces = MostCommonFace.__detect_faces(face_client, face_images)
            if not detected_faces:
                return MostCommonFace.__format_empty_result()

            most_common_face_ids = MostCommonFace.__get_most_common_face_ids(face_client, detected_faces)
            best_detected_face = MostCommonFace.__find_best_face(most_common_face_ids, detected_faces)

            return MostCommonFace.__format_result(best_detected_face)
        except APIErrorException as e:
            raise MostCommonFaceError("Face API error", e)
