from datetime import datetime
from flask import Flask, json, jsonify
from .base_model import BaseModel

class Comment(BaseModel):
    """ comments class """
    def __init__(self):
        """initialize and define objects """
        super().__init__()
      
    def create_comment(self,**kwargs):
        """" defines the logic for adding a comment """

        self.comment= kwargs['comment']
        self.username=kwargs['username']
        self.question_id=kwargs['question_id']

        user = self.get_by_key("users","username",self.username)
        check_question = self.check_if_exists("questions","id",self.question_id)
        question =self.get_by_key("questions","id",self.question_id)
      

        if not check_question:
            return jsonify({
                "status": 404,
                "error": "{} not found".format("Question")
            }), 404
        else:
            self.user_id = user[0]["id"]
            self.title = question[0]["title"]
            self.body = question[0]["body"]
            sql = """ INSERT INTO comments (user_id,question_id,comment)
                VALUES({},{},'{}') RETURNING comments.id;""".format(self.user_id,self.question_id,self.comment)
            save_comment=self.save_data(sql)
            comment =self.get_by_key("comments","id",save_comment["id"])

            return jsonify({"status": 201,
                            "data":{
                                "question":self.question_id,
                                "title":self.title,
                                "body":self.body,
                                "comment":comment[0]["comment"],
                            },
                            "message":"comment posted successfully",
                        }), 201