from flask_restful import Resource, reqparse
import models

parser = reqparse.RequestParser()
# parser.add_argument(
#     'username', help='This field cannot be blank', required=True)
# parser.add_argument(
#     'password', help='This field cannot be blank', required=True)

class PersonalDetail(Resource):
    def get(self):
        data = parser.parse_args()
        # temporary for testing, on prod remove this
        employee_id = "7187"
        personal_detail = models.PersonalDetail(employee_id)
        return personal_detail.get()