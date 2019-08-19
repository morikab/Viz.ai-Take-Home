from flask import Blueprint, request, jsonify, current_app

from vizapp.face.most_common_face.most_common_face import MostCommonFace
from vizapp.face.singleton_face_client import SingletonFaceClient
from vizapp.request_exceptions import MissingRequestJsonData, InvalidRequestException

face_blueprint = Blueprint('face', __name__)


@face_blueprint.route('/most-common-face', methods=['POST'])
def most_common_face():
    request_json_data = request.get_json()
    if request_json_data is None:
        raise MissingRequestJsonData()

    face_client = SingletonFaceClient.get_instance()

    result = MostCommonFace.most_common_face_from_image_filepaths(face_client, request_json_data)
    return jsonify(result)


@face_blueprint.errorhandler(InvalidRequestException)
def invalid_client_request(e):
    current_app.logger.error('Invalid client request: %s', str(e))
    return str(e), 400
