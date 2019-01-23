from flask import json, jsonify , make_response
import re


class Validators():
    """ global validation methods """

    def __init__(self):
        """define objects"""
        pass

    def validation_message(self,field):
        """ this method generates an empty error message for empty fields"""
        
        return make_response(jsonify({
                "status": 400,
                "error": "{} cannot be empty".format(field)
            })), 400
    

    def _validate(self,input):

        """ validate empty strings and email fields"""
        for key,value in input.items():
            if value is not None:
                if not value.strip():
                    return self.validate_whitespaces(key)
                if key == "email":
                    return self.validate_email(value)
            else:
               return self.validate_required_field(key)

    def validate_missing_data(self):
        """ validates missing json object"""

        return jsonify({'status': 400,
                        'error': "Bad request: attach missing fields"}),400

    def validate_whitespaces(self,key):
        """ return reponse for field with whitespaces"""
        return jsonify({
                        "status": 400,
                        "error": "{} cannot be empty".format(key)
                    }), 400

    def validate_email(self,value):
        """checks for a valid email"""
        if  not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                        value):
            return jsonify({'status': 400,
                        'error': "email provided is invalid"}),400
                        
    def validate_required_field(self,key):
        """returns a response for required fields"""

        return jsonify({'status': 400,
                                 "error": "{} field required".format(key)
                            }),400