from flask import Flask, jsonify, make_response
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import models
import resources
import config
import json
from aesb64 import encrypt, AESData

app = Flask(__name__)
CORS(app)
api = Api(app)
jwt = JWTManager(app)


@jwt.claims_verification_failed_loader
def my_claims_verification_failed_loader():
    return jsonify({
        'status': 400,
        'message': 'User claims verification failed'
    }), 400


@jwt.expired_token_loader
def my_expired_token_loader(expired_token):
    return jsonify({
        'status': 401,
        'message': 'Token has expired, please re-login'
    }), 401


@jwt.invalid_token_loader
def my_invalid_token_loader(error_description):
    return jsonify({
        'status': 422,
        'message': "%s, try logging in again" % error_description
    }), 422


@jwt.needs_fresh_token_loader
def my_needs_fresh_token_loader():
    return jsonify({
        'status': 401,
        'message': 'Fresh token required'
    }), 401


@jwt.revoked_token_loader
def my_revoked_token_loader():
    return jsonify({
        'status': 401,
        'message': 'Token has been revoked'
    }), 401


@jwt.unauthorized_loader
def my_unauthorized_loader(error_description):
    return jsonify({
        'status': 401,
        'message': error_description
    }), 401


@jwt.user_loader_error_loader
def my_user_loader_error_loader(identity):
    return jsonify({
        'status': 401,
        'message': 'Error loading the user %s' % identity
    }), 401


@api.representation('application/json')
def encrypt_output_json(data, code, headers=None):
    if "data" in data:
        aesdata = AESData(config.B64KEY, data["data"])
        data = {
            "data": aesdata.encrypt(),
            "message": data["message"]
        }
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp


app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES

api.add_resource(resources.Login, '/login')
api.add_resource(resources.PersonalDetail, '/myinfo/personaldetail')
api.add_resource(resources.PersonalDetailAttachment,
                 '/myinfo/personaldetail/attachment')
api.add_resource(resources.ContactDetail, '/myinfo/contactdetail')
api.add_resource(resources.ContactDetailAttachment,
                 '/myinfo/contactdetail/attachment')
api.add_resource(resources.EmergencyContact,
                 '/myinfo/emergencycontact')
api.add_resource(resources.EmergencyContactAttachment,
                 '/myinfo/emergencycontact/attachment')
api.add_resource(resources.Dependent, '/myinfo/dependent')
api.add_resource(resources.DependentAttachment, '/myinfo/dependent/attachment')
api.add_resource(resources.Job, '/myinfo/job')
api.add_resource(resources.Nationality, '/nationality')
api.add_resource(resources.WorkShift, '/workshift')
api.add_resource(resources.Religion, '/religion')
api.add_resource(resources.Country, '/country')
