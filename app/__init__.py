from flask import Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from app.database.connect import Connection
conn = Connection()
from flask import Flask, make_response, jsonify
from instance.config import app_config
from app.api.v2.views.meetup_view import meetup_v2
from app.api.v2.views.user_view import user_v2,auth_v2
from app.api.v2.views.questions_view import v2 as question_v2


def create_app(config):
    '''function creating the flask app'''

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config])
    app.register_blueprint(question_v2)
    app.register_blueprint(meetup_v2)
    app.register_blueprint(user_v2)
    app.register_blueprint(auth_v2)
    conn.init_db(app)
    try:
        conn.create_tables()
    except ValueError:
        print("could not create tabel")
    app.config['JWT_SECRET_KEY'] = "@2ekj@#02ks-"
    jwt= JWTManager(app)
    print(conn.connection)

    @app.errorhandler(404)
    def resource_not_found(message):
        """ Handling resource not found """

        return make_response(jsonify({
            "status": 404,
            "message": str(message)
        })), 404

    @app.errorhandler(400)
    def bad_request(message):
        """ Handling resource not found """

        return make_response(jsonify({
            "status": 404,
            "message": str(message)
        })), 400

    @app.errorhandler(405)
    def method_not_allowed(message):
        """ Handling method not allowed error """

        return make_response(jsonify({
            "status": 405,
            "message": str(message)
        })), 405

    @app.errorhandler(500)
    def server_internal_error(message):
        """ Handling internal server error """
        return make_response(jsonify({
            "status": 500,
            "message": str(message)
        })), 500

    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, server_internal_error)
    app.register_error_handler(400, bad_request)

    return app