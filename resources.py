from flask_restful import Resource, reqparse
import models

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'username', help='This field cannot be blank', required=True)
        parser.add_argument(
            'password', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        user = models.User(data["username"], data["password"])
        return user.login()

class PersonalDetail(Resource):
    def get(self):
        # data = parser.parse_args()
        # temporary for testing, on prod remove this
        employee_id = "7187"
        personal_detail = models.PersonalDetail(employee_id)
        return personal_detail.get()

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'first_name', help='This field cannot be blank', required=True)
        parser.add_argument(
            'middle_name', help='This field cannot be blank', required=True)
        parser.add_argument(
            'last_name', help='This field cannot be blank', required=True)
        parser.add_argument(
            'no_ktp', help='This field cannot be blank', required=True)
        parser.add_argument(
            'license_expiry_date', help='This field cannot be blank', required=True)
        parser.add_argument(
            'no_bpjs_kesehatan', help='This field cannot be blank', required=True)
        parser.add_argument(
            'no_npwp', help='This field cannot be blank', required=True)
        parser.add_argument(
            'no_bpjs_ketenagakerjaan', help='This field cannot be blank', required=True)
        parser.add_argument(
            'work_shift', help='This field cannot be blank', required=True)
        parser.add_argument(
            'gender', help='This field cannot be blank', required=True)
        parser.add_argument(
            'marital_status', help='This field cannot be blank', required=True)
        parser.add_argument(
            'nationality', help='This field cannot be blank', required=True)
        parser.add_argument(
            'religion', help='This field cannot be blank', required=True)
        parser.add_argument(
            'place_of_birth', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        # print(data)
        employee_id = "7187"
        personal_detail = models.PersonalDetail(employee_id)
        return personal_detail.put(data)