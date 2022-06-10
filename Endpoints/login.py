from flask import request, Response
import Interactions.userLogin as ul
import dbhandler as dbh
import json

# Function to log a user in. After getting password, use helper function to get the hashed+salted password. Send user data to login function
# Convert the returned data to json, and return data or error


def post():
    user_json = None
    success = False
    try:
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json['password']
        pass_hash = dbh.get_password(password, email=email, username=username)
        success, user = ul.post_login(
            email, username, pass_hash)
        user_json = json.dumps(user, default=str)
    except:
        return Response("Something went wrong logging in.", mimetype="application/json", status=403)
    if(success):
        return Response(user_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong logging in.", mimetype="application/json", status=403)
