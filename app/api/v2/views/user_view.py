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
@app.jwt_required
def get_all_users():
    ''' this endpoints allows a user to fetch all registered users'''

    return user_object.get_all_users()
   

@user_v2.route("/<int:id>", methods = ['GET'])
def get_user(id):
    ''' this endpoints allow a user to get a specific user by id'''
    return user_object.get_user_by_id(id)


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
    confirm_password =data.get('confirm_password')

    
    val_input = {"phone_number":phone_number,"firstname":firstname,"lastname":lastname,"othername":othername,"username":username,"email":email,
    "password":password,"confirm_password":confirm_password,}

    if password != confirm_password:
        return jsonify({'msg': 'confirmation password and password do not match' }), 401

    validate = validator._validate(val_input)
   
    if validate:
        return validate
    else:    

        passwordHash = generate_password_hash(password)
        data =[username,is_admin]
        access_token = app.create_access_token(identity=data)
        user_details ={"firstname":firstname,"lastname":lastname,"othername":othername,"email":email,
                    "phone_number":phone_number,"username":username,"password":passwordHash,"is_admin":is_admin,"token":access_token}
        
        user =user_object.create_user(**user_details)
        return user
 
@user_v2.route('/login', methods = ['POST'])
def login():
    """ this endpoint allows a user to login and auto-generate an auth token """
    data = request.get_json()
    # if not request.data:
    #     return validator.validate_missing_data()

    username = data.get('username')
    password = data.get('password')

    val_input = {"username":username,"password":password}
    validate = validator._validate(val_input)
    
   
    if validate:
        return validate
    else:
        user_details= val_input
        return user_object.login_user(**user_details)
      
@auth_v2.route('/token/user', methods=['GET'])
@app.jwt_required
def get_user_by_id():
    """ access identity of the current user """
    current_user = app.get_jwt_identity()
    user =user_object.get_by_key("users","username",current_user)
    return jsonify({"user":user}), 200
