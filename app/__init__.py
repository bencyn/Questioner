from flask import Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from app.database.connect import Connection
conn = Connection()

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

    return app