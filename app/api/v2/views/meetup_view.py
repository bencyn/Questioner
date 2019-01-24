from flask import Flask, json, jsonify, request, make_response, Blueprint
from datetime import datetime
from ..models import meetup_model,user_model
from ..views.user_view import user_v2
from app.api.utils.validators import Validators
import app

meetup_v2 = Blueprint('meetup_v2', __name__, url_prefix='/api/v2/meetups')
meetup_object = meetup_model.Meetup()
user_object = user_model.User()
validator = Validators()

@meetup_v2.route("/upcoming/", methods=['GET'])
def get_upcoming_meetups():
    ''' fetch all meetup records'''
    upcoming_meetups =meetup_object.get_all("meetups")
    return jsonify({
        "status":200,
        "meetup":upcoming_meetups
    }),200

@meetup_v2.route("/<int:id>", methods = ['GET'])
def get_specific_meetup(id):
    ''' this function gets a  specific meetup by id'''
    meetup =meetup_object.get_by_key("meetups","id",id)
    if meetup:
        return jsonify({
            "status":200,
            "meetup":meetup
        }),200
    else:
        return jsonify({
            "status":401,
            "error":"meetup record not found"
        }),404


@meetup_v2.route("/<int:id>", methods = ['DELETE'])
@app.jwt_required
def delete_meetup(id):
    ''' this function gets a  specific meetup by id'''
    meetup =meetup_object.get_by_key("meetups","id",id)
    if meetup:
        meetup_object.delete_by_key("meetups","id",id)  
        return jsonify({
            "status":200,
            "message":"record deleted successfully"
        }),200
    else:
        return jsonify({
            "status":401,
            "error":"meetup record not found"
        }),404

@user_v2.route('/<int:id>/meetups', methods = ['POST'])
@app.jwt_required
def create_meetup(id):
    '''this endpoints allows users to create a meetup record '''

    data = request.get_json()

    if not data:
        return jsonify({"Message": 'Cannot send empty data'}),409
    else:
        topic = data.get('topic')
        location = data.get('location')
        images = data.get('images')
        happening_on = data.get('happening_on')
        tags = data.get('tags')
        val_input = {"topic":topic,"location":location,"happening_on":happening_on,"tags":tags}

        validate = validator._validate(val_input)
        if validate:
            return validate
        else:
            meetup_details = {"topic":topic,"location":location,"images":images,"happening_on":happening_on,"tags":tags,"user_id":id}
            meetup = meetup_object.create_meetup(**meetup_details)
            return meetup



# @meetup_v2.route("/<int:meetup_id>/rsvps", methods = ['POST'])
# @app.jwt_required
# def reserveMeetup(meetup_id):
#     """ this endpoint allows a user to submit a meetup reserve response """

#     data = request.get_json()
#     try:
#         status = data.get('status')
#     except KeyError:
#         return jsonify({'status': 400,
#                         ' error': "rsvps data required"})

#     if not status.strip():
#         return validate_input("rsvps status")
#     else:
#         meetups = meetup_object.meetups
#         if meetups:
#             rsvps_meetup = meetups[meetup_id]
#             topic=rsvps_meetup["topic"]

#             return make_response(jsonify({
#                 "status":201,
#                 "data":{
#                     "topic":topic,
#                     "status":status,
#                 }
#             })), 201

#         return jsonify({"status": 404, "error": "Meetup not found"}), 404
  