from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

import models, resources

api.add_resource(resources.PersonalDetail, '/myinfo/personaldetail')