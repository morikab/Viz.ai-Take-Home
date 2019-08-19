import logging

from flask import Flask

from vizapp.face.routes import face_blueprint

BASE_CONFIG_OBJECT = 'vizapp.config.BaseConfig'


def create_app(config_object=BASE_CONFIG_OBJECT, config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)
    app.config.from_pyfile(config_filename)
    register_blueprints(app)
    configure_logger(app)
    return app


def register_blueprints(app):
    app.register_blueprint(face_blueprint, url_prefix='/face')


def configure_logger(app):
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
