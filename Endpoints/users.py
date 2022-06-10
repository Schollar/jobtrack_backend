from flask import request, Response
import json
import Interactions.userInteractions as ue
import dbhandler as dbh
import secrets
import hashlib


# Function to create password salts

def create_salt():
    return secrets.token_urlsafe(10)

# This endpoint creates a new user. Takes in requires data. It also creates a salt for the user and hashes the salted password.
# Convert the returned data to json, return the converted data in the response if success returned as true.


def post():
    user_json = None
    success = False
    try:
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        salt = create_salt()
        password = salt + password
        pass_hash = hashlib.sha512(password.encode()).hexdigest()
        success, user = ue.post_user(email, username, pass_hash, salt)
        user_json = json.dumps(user, default=str)
    except:
        return Response("Something went wrong creating a new user", mimetype="application/json", status=400)
    if(success):
        return Response(user_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong create a new user", mimetype="application/json", status=400)
