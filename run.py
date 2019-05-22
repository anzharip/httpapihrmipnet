from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import models
import resources
import config

app = Flask(__name__)
CORS(app)
api = Api(app)
jwt = JWTManager(app)

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
