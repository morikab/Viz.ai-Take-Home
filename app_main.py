from flask import Flask

from most_common_face import most_common_face_blueprint

# TODO - improvements:
#   * responses in case of failures
#   * requirements.txt file
#   * Logger
#   * tests (empty picture list, picture with no faces, very long list, very loaded picture..)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(most_common_face_blueprint)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8001)  # TODO - move port to server configuration
