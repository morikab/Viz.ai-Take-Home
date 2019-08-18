from flask import Flask

from app.face.routes import face_blueprint


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_pyfile(config_filename)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(face_blueprint, url_prefix='/face')
