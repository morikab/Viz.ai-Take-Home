from flask import Blueprint, request, current_app as app

from detected_face import DetectedFace
from face_image import FaceImage
from singleton_face_client import SingletonFaceClient


# TODO - think again about exceptions' design (and location)
class InvalidRequestException(Exception):
    pass


class MissingRequestJsonData(InvalidRequestException):
    pass


class MissingRequestImagesData(InvalidRequestException):
    pass


class InvalidRequestImagesDataFormat(InvalidRequestException):
    pass


class EmptyRequestImagesData(InvalidRequestException):
    pass


most_common_face_blueprint = Blueprint('most_common_face', __name__)

REQUEST_IMAGES_KEY = "images"


def get_images_filepaths(request_json_data):
    if REQUEST_IMAGES_KEY not in request_json_data:
        raise MissingRequestImagesData()

    images = request_json_data[REQUEST_IMAGES_KEY]

    if not isinstance(images, list):
        raise InvalidRequestImagesDataFormat()
    if not images:
        raise EmptyRequestImagesData()

    return images


def detect_faces(face_client, face_images):
    total_detected_faces = []

    for face_image in face_images:
        with face_image.image_stream() as image_stream:
            # TODO - wrap with try-catch (API error)
            faces_metadata = face_client.face.detect_with_stream(image_stream, return_face_id=True,
                                                                 return_face_landmarks=True)
            detected_faces = [DetectedFace(face_metadata, face_image) for face_metadata in faces_metadata]
            total_detected_faces.extend(detected_faces)

    return total_detected_faces


def find_best_face_in_group(group, detected_faces):
    group_detected_faces = []

    for face_id in group:
        for face in detected_faces:
            if face.metadata.face_id == face_id:
                group_detected_faces.append(face)
                break  # TODO - add check that all group faces were found?

    return max(group_detected_faces, key=lambda detected_face: detected_face.face_image_ratio)


@most_common_face_blueprint.route('/most-common-face', methods=['POST'])
def most_common_face():
    request_json_data = request.get_json()
    if request_json_data is None:
        raise MissingRequestJsonData()  # ODO - return more indicative error message (to client)

    images_filepaths = get_images_filepaths(request_json_data)
    face_images = [FaceImage(filepath) for filepath in images_filepaths]

    face_client = SingletonFaceClient.get_instance()

    detected_faces = detect_faces(face_client, face_images)
    if not detected_faces:
        return None    # FIXME - raise exception

    # TODO - handle case where number of faces is not supported by API (<2 OR >1000)
    detected_face_ids = [face.id for face in detected_faces]

    group_result = face_client.face.group(detected_face_ids)
    if not group_result.groups:
        return None     # FIXME - find correct syntax

    # groups are ranked (==sorted?) by their size # TODO - verify this
    best_face = find_best_face_in_group(group_result.groups[0], detected_faces)

    return best_face.metadata  # TODO - make sure this is the right response format
