from flask import Flask, json, jsonify, request, make_response, Blueprint
from datetime import datetime
import app,re
from ..models import comments_model
from ....api.v2 import v2
from app.api.utils.validators import Validators

validator = Validators()
comment_object = comments_model.Comment()

@v2.route("/questions/<int:question_id>/comments", methods=['POST'])
@app.jwt_required
def create_comment(question_id):
    """ post method that creates a comment posted to a specific question """

    data = request.get_json()

    comment = data.get('comment')
    current_user = app.get_jwt_identity()
    val_input = {"comment":comment}

    validate = validator._validate(val_input)
    if validate:
        return validate
    else:
        comment_details = {"comment":comment,"username":current_user,"question_id":question_id}
        comment = comment_object.create_comment(**comment_details)
        return comment
