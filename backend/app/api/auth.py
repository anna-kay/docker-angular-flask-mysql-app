from flask import Blueprint, Response, request, json
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required, get_jwt, decode_token
from ..database.authManager import AuthManager
from datetime import timedelta
import redis
from .extensions import jwt

authAPI = Blueprint('authAPI', __name__)
endpoint = "/auth"
access_token_expiration_time = 1800 #seconds
refresh_token_expiration_time = 1 #day

auth_manager = AuthManager()

# Setup our redis connection for storing the blocklisted tokens. You will probably
# want your redis instance configured to persist data to disk, so that a restart
# does not cause your application to forget that a JWT was revoked.
jwt_redis_blocklist = redis.StrictRedis(host= "redis", port=6379, db=0, decode_responses=True)

# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

@authAPI.route(endpoint + "/login", methods=['POST'])
def login():
    result = {}
    try:
        
        data = json.loads(request.data.decode())
        user = auth_manager.retrieve_user(data)        
        
        if len(user) > 0:
            result = create_jwt_payload(user)
            response = Response(json.dumps({"data": result}), mimetype='application/json', status=200)
        else:
            response = Response(json.dumps({"data": []}), mimetype='application/json', status=401)
    except Exception as e:
        response = handleException(e)
    finally:
        return response

@authAPI.route(endpoint + "/refresh-token", methods=['POST'])
def refresh_token():
    try:
        previous_refresh_token = decode_token(json.loads(request.data.decode())["token"]["refresh_token"])
        result = create_jwt_payload(previous_refresh_token["identity"])
        response = Response(json.dumps({"data": result}), mimetype='application/json', status=200)
    except Exception as e:
        response = handleException(e)
    finally:
        return response

@authAPI.route(endpoint + "/logout", methods=['DELETE'])
@jwt_required()
def logout():    
    try:
        result = json.dumps({})
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=access_token_expiration_time)
        # return jsonify(msg="Access token revoked")      
        response = Response(result, mimetype='application/json', status=200)
    except Exception as e:
        response = handleException(e)
    finally:
        return response

@authAPI.route(endpoint + "/register", methods=['POST'])
def register():
    try:
        data = json.loads(request.data.decode())
        user = auth_manager.store_user(data)
        result = create_jwt_payload(user)
        response = Response(json.dumps({"data": result}), mimetype='application/json', status=200)
    except Exception as e:
        response = handleException(e)
    finally:
        return response

@authAPI.route(endpoint + "/forgot_password", methods=['POST'])
def forgot_password():
    try:
        data = json.loads(request.data.decode())
        result = json.dumps(data)
        response = Response(result, mimetype='application/json', status=200)
    except Exception as e:
        response = handleException(e)
    finally:
        return response

def create_jwt_payload(data):
    access_token = create_access_token(identity=data, expires_delta=timedelta(seconds=access_token_expiration_time)) 
    refresh_token = create_refresh_token(identity=data, expires_delta=timedelta(days=refresh_token_expiration_time))

    payload = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": access_token_expiration_time,
            "token_type": "Bearer",
            }
    return payload


def handleException(e):
    result = json.dumps({"error": str(e)})
    print("=======================================" + result + "=======================================" )
    return Response(result, mimetype='application/json', status=500)
