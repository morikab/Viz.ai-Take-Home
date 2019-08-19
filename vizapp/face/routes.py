from flask import Blueprint, request, jsonify, current_app

from vizapp.face.most_common_face.most_common_face import MostCommonFace, MostCommonFaceError
from vizapp.face.singleton_face_client import SingletonFaceClient
from vizapp.request_exceptions import MissingRequestJsonData, InvalidRequestException

face_blueprint = Blueprint('face', __name__)


@face_blueprint.route('/most-common-face', methods=['POST'])
def most_common_face():
    current_app.logger.info('Handling new most-common-face request') # TODO - check this

    request_json_data = request.get_json()
    if request_json_data is None:
        raise MissingRequestJsonData()

    face_client = SingletonFaceClient.get_instance(current_app.config)

    result = MostCommonFace.most_common_face_from_image_filepaths(face_client, request_json_data)
    return jsonify(result)


def detailed_error_message(e):
    if e.cause() is not None:
        return str(e) + ": " + e.cause()
    return str(e)


@face_blueprint.errorhandler(InvalidRequestException)
def invalid_client_request(e):
    current_app.logger.error('Invalid client request: %s', detailed_error_message(e))
    return {"error": str(e), "details": e.cause()}, 400


@face_blueprint.errorhandler(MostCommonFaceError)
def most_common_face_error(e):
    current_app.logger.error('Most common face internal error: %s', detailed_error_message(e))
    return {"error": str(e), "details": e.cause()}, 500


@face_blueprint.errorhandler(Exception)
def unknown_error(e):
    current_app.logger.error('Unknown error: %s', str(e))
    return {"error": "Unknown server error", "details": None}, 500
