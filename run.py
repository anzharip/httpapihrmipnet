from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
import models
import resources

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config['SECRET_KEY'] = 'some-secret-string'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
# app.config['JWT_BLACKLIST_ENABLED'] = True
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# @jwt.token_in_blacklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return models.RevokedTokenModel.is_jti_blacklisted(jti)

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
api.add_resource(resources.DependentAttachment, '/myinfo/dependent/attachment')
api.add_resource(resources.SecretResource, '/secret')
