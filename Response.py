from flask import Response as FlaskResponse
from flask import jsonify
import json

"""
Custom response class that allows us to set defaults on outgoing response messages,
and also manipulate the responses to Flask Response class compatible types.

NOTE: If "status" is included as key in json object and is an int, it will be used as the HTTP status code for that response.
This allows us to pass status codes from services without importing the Response class.
"""

class Response(FlaskResponse):

    def __init__(self, response=None, **kwargs):

        if (isinstance(response, str)):
            response = json.dumps({"message": response})
        
        if (isinstance(response, dict) and "status" in response and isinstance(response["status"], int)): 
            kwargs["status"] = response["status"]
            response.pop("status")

        if("content_type" not in kwargs):
            kwargs["content_type"] = "application/json"
        
        kwargs["headers"] = {"Access-Control-Allow-Credentials": "true"}
        return super(Response, self).__init__(response,**kwargs)

    """
    Allows python dictionary objects to be returned as JSON automatically
    """
    @classmethod
    def force_type(cls, rv, environ=None):
        if (isinstance(rv, dict)):
            rv = jsonify(rv)
        return super(Response, cls).force_type(rv,environ)