from flask import Flask, request, Response
import dbhandler as dbh
import sys
app = Flask(__name__)


# Setting up an authenticator function that will run before all endpoints to see if user is authenticated with the correct logintoken
# Before requests that are decorated with @authenticate, this will grab the login token from the cookie and verify the logintoken exists and is valid. If so it continues on to the endpoint requested, if not it errors before getting to the endpoint


@app.before_request
def validate_token():
    if(request.method.lower() == 'options'):
        return
    if(request.endpoint in app.view_functions):
        if(hasattr(app.view_functions[request.endpoint], 'must_authenticate')):
            success = dbh.validate_login_token(
                request.cookies.get('logintoken'))
            if(success == False):
                return Response('Invalid Login Token', mimetype="plain/text", status=403)


def authenticate(endpoint):
    endpoint.must_authenticate = True
    return endpoint


# Checking to see if a mode was passed to the script
if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print('You must pass a mode to run this script. Either testing or production')
    exit()
# Depending on what mode is passed, we check and run the appropriate code.
if(mode == "testing"):
    print('Running in testing mode!')
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
elif(mode == "production"):
    print('Running in production mode')
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5006)
else:
    print('Please Run in either testing or production')
