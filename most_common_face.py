from flask import Blueprint, request, current_app as app

from face_api_client import FaceApiClient


class InvalidRequestException(Exception):
    pass


class MissingRequestJsonData(InvalidRequestException):
    pass


class MissingRequestImagesData(InvalidRequestException):
    pass


most_common_face_blueprint = Blueprint('most_common_face', __name__)


@most_common_face_blueprint.route('/most-common-face', methods=['POST'])
def most_common_face():
    request_data = request.get_json()

    if request_data is None:
        raise MissingRequestJsonData  # TODO - return more indicative error message (to client)

    if "images" not in request_data or not request_data["images"]:
        raise MissingRequestImagesData

    images = request_data["images"]
    face_api_client = FaceApiClient.get_instance()

    return face_api_client.most_common_face(images)  # TODO - delegate or implement?
