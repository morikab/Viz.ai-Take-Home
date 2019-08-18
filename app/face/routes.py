from flask import Blueprint, request, jsonify

from app.face.most_common_face.most_common_face import MostCommonFace
from app.face.singleton_face_client import SingletonFaceClient
from app.request_exceptions import MissingRequestJsonData, MissingRequestDataKey, InvalidRequestDataFormat

face_blueprint = Blueprint('face', __name__)

REQUEST_IMAGES_KEY = "images"


@face_blueprint.route('/most-common-face', methods=['POST'])
def most_common_face():
    request_json_data = request.get_json()
    if request_json_data is None:
        raise MissingRequestJsonData()  # ODO - return more indicative error message (to client)

    if REQUEST_IMAGES_KEY not in request_json_data:
        raise MissingRequestDataKey()   # TODO - add key as parameter to class

    image_filepaths = request_json_data[REQUEST_IMAGES_KEY]
    if not isinstance(image_filepaths, list):
        raise InvalidRequestDataFormat()     # TODO - add key and type as parameter to class

    face_client = SingletonFaceClient.get_instance()

    result = MostCommonFace.most_common_face_from_image_filepaths(face_client, image_filepaths)

    return jsonify(result)
