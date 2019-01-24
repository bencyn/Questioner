# import psycopg2, os
# from app.database.connect import db_init
from flask import Flask, json, jsonify
from .base_model import BaseModel


class Meetup(BaseModel):
    """ meetup class """

    def __init__(self):
        """initialize and define objects """
        super().__init__()
    def create_meetup(self,**kwargs):
        """ create a meetup record """
        self.topic= kwargs['topic']
        self.location= kwargs['location']
        self.images= kwargs['images']
        self.happening_on= kwargs['happening_on']
        self.tags= kwargs['tags']
        self.user_id= kwargs['user_id']
        
        user = self.get_by_key("users","id",self.user_id)

        if user:
            admin = user[0]["is_admin"] 
            if admin == "1":
                sql = """ INSERT INTO meetups (happening_on,location,images,topic,tags,user_id)
                        VALUES('{}','{}','{}','{}','{}','{}') RETURNING meetups.id;""".format(self.happening_on,self.location,self.images,self.topic,
                         self.tags,self.user_id)

                save_meetup=self.save_data(sql)
                meetup = self.get_by_key("meetups","id",save_meetup["id"])

                return jsonify({ 
                    "status": 201,
                    "data":meetup,
                    "message":"meetup record created successfully",
                }), 201
            else:
                return jsonify({'msg': 'user is not an admin' }), 401
        else:
            return jsonify({'msg': 'user does not exist' }), 404

        
   
    def login_user(self):
        """"""
        pass
  