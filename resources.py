from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import models
from base64 import b64encode


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'username', help='This field cannot be blank', required=True)
        parser.add_argument(
            'password', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        user = models.User(data["username"], data["password"])
        if user.get() is None:
            return {
                "message": "Username not found"
            }
        emp_number = user.get()[0]
        if user.verify_hash() is True:
            access_token = create_access_token(identity=emp_number)
            refresh_token = create_refresh_token(identity=emp_number)
            return {
                'message': 'Logged in as {}'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {
                "message": "Username & password does not match"
            }


class PersonalDetail(Resource):
    @jwt_required
    def get(self):
        # data = parser.parse_args()
        # temporary for testing, on prod remove this
        emp_number = get_raw_jwt()['identity']
        # employee_id = "7187"
        personal_detail = models.PersonalDetail(emp_number)
        return personal_detail.get()

    @jwt_required
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
        # employee_id = "7187"
        emp_number = get_raw_jwt()['identity']
        personal_detail = models.PersonalDetail(emp_number)
        return personal_detail.put(data)


class PersonalDetailAttachment(Resource):
    def __init__(self):
        self.screen = "personal"

    @jwt_required
    def get(self):
        emp_number = get_raw_jwt()['identity']
        attachment = models.Attachment(emp_number, self.screen)
        parser = reqparse.RequestParser()
        parser.add_argument(
            'file_id', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        if data["file_id"] == "all":
            result = []
            for attachment in attachment.get_meta_all():
                result.append(
                    {
                        "file_id": attachment[1],
                        "comment": attachment[2],
                        "file_name": attachment[3],
                        "size": attachment[4],
                        "type": attachment[5],
                        "date_added": attachment[9],
                        "message": "File succesfully retrieved"
                    }
                )
            return result
        else:
            result = attachment.get(data["file_id"])
            if result is None:
                return {
                    "message": "File not found"
                }
            else:
                return {
                    "file_id": result[1],
                    "file": b64encode(result[5]).decode(),
                    "comment": result[2],
                    "file_name": result[3],
                    "size": result[4],
                    "type": result[6],
                    "date_added": result[10],
                    "message": "File succesfully retrieved"
                }

    @jwt_required
    def post(self):
        emp_number = get_raw_jwt()['identity']
        parser = reqparse.RequestParser()
        parser.add_argument(
            'select_file', help='This field cannot be blank', required=True)
        parser.add_argument(
            'file_name', help='This field cannot be blank', required=True)
        parser.add_argument(
            'comment', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        attachment = models.Attachment(emp_number, self.screen)
        return attachment.post(data)

    @jwt_required
    def put(self):
        emp_number = get_raw_jwt()['identity']
        parser = reqparse.RequestParser()
        parser.add_argument(
            'file_id', help='This field cannot be blank', required=True)
        parser.add_argument(
            'comment', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        attachment = models.Attachment(emp_number, self.screen)
        if attachment.put_comment(data) == 0:
            return {
                "message": "Comment not updated or no file_id found"
            }
        else:
            result = {
                "file_id": data['file_id'],
                "comment": data['comment'],
                "message": "Comment succesfully updated"
            }
            return result

    @jwt_required
    def delete(self):
        emp_number = get_raw_jwt()['identity']
        parser = reqparse.RequestParser()
        parser.add_argument(
            'file_id', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        attachment = models.Attachment(emp_number, self.screen)
        if attachment.delete(data['file_id']) == 0:
            return {
                "message": "No file_id found"
            }
        else:
            result = {
                "file_id": data['file_id'],
                "message": "File succesfully deleted"
            }
            return result


class ContactDetailAttachment(PersonalDetailAttachment):
    def __init__(self):
        self.screen = "contact"


class EmergencyContactAttachment(PersonalDetailAttachment):
    def __init__(self):
        self.screen = "emergency"


class DependentAttachment(PersonalDetailAttachment):
    def __init__(self):
        self.screen = "dependent"


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
