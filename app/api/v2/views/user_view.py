from flask import Flask, json, jsonify, request, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import app,re
from app.api.v2.models import user_model
from app.api.utils.validators import Validators

user_v2 = Blueprint('user_v2', __name__, url_prefix='/api/v2/auth')
auth_v2 = Blueprint('auth_v2',__name__, url_prefix='/api/v2/auths')

user_object = user_model.User()
validator = Validators()

@user_v2.route("/all", methods=['GET'])
def get_all_users():
    ''' this endpoints allows a user to fetch all registered users'''
    all_users = user_object.get_all("users")
    return jsonify({
        "status":200,
        "users":all_users
    }),200

@user_v2.route("/<int:id>", methods = ['GET'])
def get_user(id):
    ''' this endpoints allow a user to get a specific user by id'''
    user =user_object.get_by_key("users","id",id)
    if user:
        return jsonify({
            "status":200,
            "user":user
        }),200
    else:
        return jsonify({
            "status":404,
            "error":"User not found"
        }),404
   

@user_v2.route('/signup', methods = ['POST'])
def register():
    """ this endpoint allows unregistered users to signup """
    data = request.get_json()

    if not data:
        return jsonify({"Message": 'Cannot send empty data'}),409
    
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    othername = data.get('othername')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')
    username = data.get('username')
    is_admin = data.get('is_admin')
    
    val_input = {"firstname":firstname,"lastname":lastname,"username":username,
        "email":email,"password":password}
   
    validate = validator._validate(val_input)
   
    if validate:
        return validate
    else:    
        passwordHash = generate_password_hash(password)
        access_token = app.create_access_token(identity=username)
        user_details ={"firstname":firstname,"lastname":lastname,"othername":othername,"email":email,
                    "phone_number":phone_number,"username":username,"password":passwordHash,"is_admin":is_admin,"token":access_token}
        
        user =user_object.create_user(**user_details)
        return user
 
@user_v2.route('/login', methods = ['POST'])
def login():
    """ this endpoint allows a user to login and auto-generate an auth token """
    data = request.get_json()
    if not request.data:
        return validator.validate_missing_data()

    username = data.get('username')
    password = data.get('password')
    # confirm_password = request.get_json()['confirm_password']


    val_input = {"username":username,"password":password}
    validate = validator._validate(val_input)
   
    if validate:
        return validate
    else:
        user = user_object.get_by_key("users","username",username)
        if user:
            validate_password = check_password_hash(user[0]["password"], password)
            if validate_password:
                jwt_token = app.create_access_token(identity=username)
                return jsonify({ 
                    "status": 201,
                    "data":[{"token":jwt_token,"user":user}],
                    "message":"user logged in successfully",
                }), 201
            return jsonify({'msg': 'incorrect username/password combination' }), 401
        else:
            return jsonify({'msg': 'user does not exist' }), 404
        

@auth_v2.route('/token', methods=['GET'])
@app.jwt_required
def protected():
    """ access identity of the current user """
    current_user = app.get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
