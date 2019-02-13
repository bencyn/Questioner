from datetime import datetime
from flask import Flask, json, jsonify
from .base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
import app,re
class User(BaseModel):
    """ user class """

    def __init__(self):
        """initialize and define objects """
        BaseModel().__init__()
        
    def create_user(self,**kwargs):
        """ create a user account in users table """
        
        self.firstname= kwargs['firstname']
        self.lastname= kwargs['lastname']
        self.othername= kwargs['othername']
        self.email= kwargs['email']
        self.phone_number= kwargs['phone_number']
        self.username= kwargs['username']
        self.password= kwargs['password']
        self.registered= str(datetime.now())
        self.is_admin=kwargs.get('is_admin','0')

        sql = """ INSERT INTO users (firstname,lastname,othername,email,phone_number,username,password,is_admin)
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}') RETURNING users.id;""".format(self.firstname,self.lastname,self.othername,self.email,self.phone_number,self.username,
                                    self.password,self.is_admin)

        check_username = self.check_if_exists("users","username",self.username)
        check_email = self.check_if_exists("users","email",self.email)

        if check_username:
            return jsonify({
                "status": 400,
                "error": "{} already exists".format("username")
            }), 400
        elif check_email:
            return jsonify({
                "status": 400,
                "error": "{} already exists".format("email")
            }), 400
        else:
            save_user=self.save_data(sql)
            user = self.get_by_key("users","id",save_user["id"])

            return jsonify({"status": 201,
                    "message":"user registered successfully",
                    "username":user[0]["username"],
                }), 201
   
    def login_user(self,**kwargs):
        """ validates user then login"""
        self.username = kwargs['username']
        self.password = kwargs['password']

        user = self.get_by_key("users","username",self.username)
        if user:
            validate_password = check_password_hash(user[0]["password"], self.password)
            if validate_password:
                jwt_token = app.create_access_token(identity=user[0])
                return jsonify({ 
                    "status": 201,
                    "data":[{"token":jwt_token}],
                    "message":"user logged in successfully",
                }), 201
            return jsonify({'error': 'incorrect username/password combination' }), 401
        else:
            return jsonify({'error': 'user does not exist' }), 404

    def get_all_users(self):
        """ get all users """

        all_users = self.get_all("users")
        key="users"
        error = "No users registered"
        return self.message_response(all_users,error,key)
      

    def get_user_by_id(self,id):
        """ get a specific by users id"""

        user =self.get_by_key("users","id",id)
        feeds =self.user_profile(id,status="feeds")
        questions_posted=self.user_profile(id,status="posted")
        questions_commented =self.user_profile(id,status="commented")

        key="user"
        error = "User not found"
        # return self.message_response(user,error,key)
        if user:
            return jsonify({
                "status":200,
                "{}".format(key):user,
                "feeds":feeds,
                "questions_posted":questions_posted,
                "questions_commented":questions_commented
            }),200
        else:
            return jsonify({
                "status":404,
                "error":error
            }),404
      
   
    def message_response(self,value,error,key):
        """return message if true or false"""
        if value:
            return jsonify({
                "status":200,
                "{}".format(key):value
            }),200
        else:
            return jsonify({
                "status":404,
                "error":error
            }),404