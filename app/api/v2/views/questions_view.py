from flask import Flask, json, jsonify, request, make_response, Blueprint
from datetime import datetime
import app
from ..models import questions_model,meetup_model,user_model
from ....api.v2 import v2
from app.api.utils.validators import Validators

validator = Validators()
question_object=questions_model.Question()
meetup_object = meetup_model.Meetup()
user_object = user_model.User()


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
        user_id = data.get('user_id')
        val_input = {"title":title,"body":body,"user_id":user_id}
    
        validate = validator._validate(val_input)
        if validate:
            return validate
        else:
            question_details = {"title":title,"body":body,"meetup_id":meetup_id,"user_id":user_id}
            question = question_object.create_question(**question_details)
            return question


@v2.route("/questions/<int:question_id>/upvote", methods=['PATCH'])
@app.jwt_required
def upvote_question(question_id):
    """ question upvote endpoint logic """
    current_user = app.get_jwt_identity()
    vote_details = {"username":current_user,"question_id":question_id}
    upvote = question_object.upvote_question(**vote_details)
    return upvote
  

@v2.route("/questions/<int:question_id>/downvote", methods=['PATCH'])
@app.jwt_required
def downvote_question(question_id):
    """ question downvote endpoint logic """
    current_user = app.get_jwt_identity()
    vote_details = {"username":current_user,"question_id":question_id}
    downvote = question_object.downvote_question(**vote_details)
    return downvote
  