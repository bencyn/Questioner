from flask import Flask, json, jsonify, request, make_response, Blueprint
from datetime import datetime
from ..models import meetup_model

meetup_v2 = Blueprint('meetup_v2', __name__, url_prefix='/api/v2/meetups')
meetup_object = meetup_model.Meetup()

@meetup_v2.route("/upcoming/", methods=['GET'])
def getMeetups():
    ''' fetch all meetup records'''
    return jsonify(meetup_object.get_meetups()),200

@meetup_v2.route("/<int:id>", methods = ['GET'])
def getMeetup(id):
    ''' this function gets a  specific meetup by id'''
    return jsonify(meetup_object.get_meetup(id)),200

@meetup_v2.route('/', methods = ['POST'])
def create_meetup():
    '''this endpoints allows users to create a meetup record '''

    data = request.get_json()

    if not data:
        return jsonify({"Message": 'Cannot send empty data'}),409
    else:
        topic = data.get('topic')
        location = data.get('location')
        images = data.get('images')
        happeningOn = data.get('happeningOn')
        tags = data.get('tags')
        
        val_input = {"topic":topic,"location":location,"happeningOn":happeningOn,"tags":tags}

        for key,value in val_input.items():
            if  not value.strip() :
                return make_response(jsonify({
                    "status": 400,
                    "error": "{} cannot be empty".format(key)
                })), 400
                
        # pass user input
        user_input = {"topic":topic,"location":location,"images":images,"happeningOn":happeningOn,"tags":tags}
        meetup = meetup_object.add_meetup(user_input)
        return jsonify({"status": 201,"data":meetup}), 201

@meetup_v2.route("/<int:meetup_id>/rsvps", methods = ['POST'])
def reserveMeetup(meetup_id):
    """ this endpoint allows a user to submit a meetup reserve response """

    data = request.get_json()
    try:
        status = data.get('status')
    except KeyError:
        return jsonify({'status': 400,
                        ' error': "rsvps data required"})

    if not status.strip():
        return validate_input("rsvps status")
    else:
        meetups = meetup_object.meetups
        if meetups:
            rsvps_meetup = meetups[meetup_id]
            topic=rsvps_meetup["topic"]

            return make_response(jsonify({
                "status":201,
                "data":{
                    "topic":topic,
                    "status":status,
                }
            })), 201

        return jsonify({"status": 404, "error": "Meetup not found"}), 404
  
def validate_input(field):
    """ returns an empty error message"""

    return make_response(jsonify({
        "status": 400,
        "message": "{} cannot be empty".format(field)
    })), 400