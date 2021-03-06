from flask import json, jsonify , make_response
import re


class Validators():
    """ global validation methods """

    def __init__(self):
        """define objects"""
        pass

    def validation_message(self,field):
        """ this method generates an empty error message for empty fields"""
        error = "{} cannot be empty".format(field)
        return self.get_response(error)
    
  
    def _validate(self,input):

        """ validate empty strings and email fields"""
        regex = '[a-zA-Z0-9]'

        for key,value in input.items():
            if value is not None:
                if not value.strip():
                    error ="{} cannot be empty".format(key)
                    return self.get_response(error)

                if key !="phone_number" and not re.match(regex,value):
                    error ="{} input contains invalid characters".format(key)
                    return self.get_response(error)

                if key == "email":
                    return self.validate_email(value)

                if key == "phone_number":
                    if value[0] == '+':
                        if not value[1:].isdigit(): 
                            error ="phone number invalid"
                            return self.get_response(error)
                    elif value[0] == '0':
                        if len(value) != 10:
                            error ="phone number invalid"
                            return self.get_response(error)
                    
                    elif value[0] != '0':
                        if len(value) != 9:
                            error ="phone number invalid"
                            return self.get_response(error)

                            
            else:
                error ="{} field required".format(key)
                return jsonify({'status': 400,
                        "error": error
                    }),400


    def validate_whitespace(self,value,key):
        """checks for whitespace in values"""
        pass

    def validate_email(self,value):
        """checks for a valid email"""
        if  not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                        value):
            error = "email provided is invalid"
            return self.get_response(error)
    
    def validate_phone_number(self,value,key):
        """ checks for a valid phonenumber"""
        if not re.match(r'^(?:\+?)?[07]\d{9,13}$' ,value):
            error ="{} invalid".format(key)
            return self.get_response(error)

    def get_response(self,error):
        """returns an error response based on the error values"""

        return jsonify({'status': 400,
                        "error": error
                    }),400