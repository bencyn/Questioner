from flask import Flask, json, jsonify, request, make_response, Blueprint
from datetime import datetime
from app.api.v1.models import user_model
from app.api.utils.validators import Validators
import app,re

user = Blueprint('user', __name__, url_prefix='/api/v1/users')
auth = Blueprint('auth',__name__, url_prefix='/api/v1/auth')
user_object = user_model.User()
validator = Validators()

@user.route("/all", methods=['GET'])
@app.jwt_required
def getUsers():
    ''' this endpoints allows a user fetch all registered users'''
    return jsonify(user_object.get_users()),200

@user.route("/<int:id>", methods = ['GET'])
@app.jwt_required
def getMeetup(id):
    ''' this endpoints allows a user get a specific meetup'''
    return jsonify(user_object.get_user(id)),200

@user.route('/', methods = ['POST'])
def register():
    """ this endpoint allows unregistered users to signup """
    data = request.get_json()

    if not data:
        return jsonify({"Message": 'Cannot send empty data'}),409
    
    firstname = request.get_json()['firstname']
    lastname = request.get_json()['lastname']
    othername = request.get_json()['othername']
    email = request.get_json()['email']
    phoneNUmber = request.get_json()['phoneNUmber']
    password = request.get_json()['password']
    username = request.get_json()['username']
    isAdmin = request.get_json()['isAdmin']

    val_input = {"username":username,"email":email,"password":password}

    for key,value in val_input.items():
        if not value.strip():
            return make_response(jsonify({
                "status": 400,
                "error": "{} cannot be empty".format(key)
            })), 400
            
        if key == "email":
            if  not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                value):
                return jsonify({'status': 400,
                            'error': "email provided is invalid"}),400
    user_details ={"firstname":firstname,"lastname":lastname,"othername":othername,"email":email,
                    "phone_number":phoneNUmber,"password":password,"username":username,"is_admin":isAdmin}
        
    user = user_object.create_user(**user_details)
    
    return jsonify({
        "status": 201,
        "data":user
    }), 201


@user.route('/login', methods = ['POST'])
def login():
    """ this endpoint allows a user to login and auto-generate an auth token """

    if not request.data:
        return validator.validate_missing_data()

    username = request.get_json()['username']
    password = request.get_json()['password']
    
    val_input = {"username":username,"password":password}

    for key,value in val_input.items():
        if not value.strip():
            return make_response(jsonify({
                "status": 400,
                "error": "{} cannot be empty".format(key)
            })), 400

    users = user_object.users
    
    if any(y['username'] == username for y in users) and any(y['password'] == password for y in users):
        access_token = app.create_access_token(identity=username)
        user_loggedIn = user_object.login_user(username,password,access_token)
        
        return jsonify({ "status": 201,
                        "message":"user logged in successfully",
                        "data":user_loggedIn,}), 201
    else:
        return jsonify({'msg': 'incorrect username/password combination' }), 401

@auth.route('/token', methods=['GET'])
@app.jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = app.get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


