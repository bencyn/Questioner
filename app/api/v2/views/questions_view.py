from flask import Flask, json, jsonify, request, make_response, Blueprint
from datetime import datetime
import app,re
from ..models import questions_model,meetup_model,user_model
from ....api.v2 import v2
from app.api.utils.validators import Validators

validator = Validators()
question_object=questions_model.Question()
meetup_object = meetup_model.Meetup()
user_object = user_model.User()


@v2.route("/questions/all", methods=['GET'])
def get_all_questions():
    ''' fetch all question records'''
    questions =question_object.get_all("questions")
    return jsonify({
        "status":200,
        "question":questions
    }),200

@v2.route("/meetups/<int:meetup_id>/questions", methods=['POST'])
@app.jwt_required
def create_question(meetup_id):
    """ post method that creates a question posted in a specific meeting """

    data = request.get_json()

    if not data:
        return jsonify({"Message": 'Cannot send empty data'}),409
    else:
        title = data.get('title')
        body = data.get('body')
        current_user = app.get_jwt_identity()
        val_input = {"title":title,"body":body}
    
        validate = validator._validate(val_input)
        if validate:
            return validate
        else:
            question_details = {"title":title,"body":body,"meetup_id":meetup_id,"username":current_user["username"]}
            question = question_object.create_question(**question_details)
            return question


@v2.route("/questions/<int:question_id>/upvote", methods=['PATCH'])
@app.jwt_required
def upvote_question(question_id):
    """ question upvote endpoint logic """
    current_user = app.get_jwt_identity()
    return question_object.upvote_question(current_user["username"],question_id)
  

@v2.route("/questions/<int:question_id>/downvote", methods=['PATCH'])
@app.jwt_required
def downvote_question(question_id):
    """ question downvote endpoint logic """
    current_user = app.get_jwt_identity()
    return question_object.downvote_question(current_user["username"],question_id)
  