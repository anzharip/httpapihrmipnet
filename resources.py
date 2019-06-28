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
        try:
            if user.get() is None:
                return {
                    "message": "Username not found"
                }, 400
            emp_number = user.get()[0]
            if user.verify_hash() is True:
                access_token = create_access_token(identity=emp_number)
                return {
                    'message': 'Logged in as {}'.format(data['username']),
                    'access_token': access_token
                }
            else:
                return {
                    "message": "Username & password does not match"
                }, 400
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class PersonalDetail(Resource):
    @jwt_required
    def get(self):
        emp_number = get_raw_jwt()['identity']
        try:
            personal_detail = models.PersonalDetail(emp_number)
            return {
                "data": personal_detail.get(),
                "message": "Personal detail succesfully retrieved"
            }
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

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
        emp_number = get_raw_jwt()['identity']
        try:
            personal_detail = models.PersonalDetail(emp_number)
            if personal_detail.put(data) == 0:
                return {
                    "message": "Personal detail not updated, no change found on submitted data"
                }
            else:
                result = {
                    "message": "Personal detail succesfully updated"
                }
                return result
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class Attachment(Resource):
    def __init__(self):
        self.screen = ""

    @jwt_required
    def get(self):
        emp_number = get_raw_jwt()['identity']
        attachment = models.Attachment(emp_number, self.screen)
        parser = reqparse.RequestParser()
        parser.add_argument(
            'file_id', help='This field cannot be blank', required=True, location=["form", "args"])
        data = parser.parse_args()
        try:
            if data["file_id"] == "all":
                result = []
                for attachment in attachment.get_meta_all():
                    result.append(
                        {
                            "file_id": str(attachment[1]),
                            "comment": attachment[2],
                            "file_name": attachment[3],
                            "size": str(attachment[4]),
                            "type": attachment[5],
                            "date_added": attachment[9]
                        }
                    )
                return {
                    "data": result,
                    "message": "Files succesfully retrieved"
                }
            else:
                result = attachment.get(data["file_id"])
                if result is None:
                    return {
                        "message": "File not found"
                    }, 400
                else:
                    return {
                        "data": {
                            "file_id": result[1],
                            "file": b64encode(result[5]).decode(),
                            "comment": result[2],
                            "file_name": result[3],
                            "size": result[4],
                            "type": result[6],
                            "date_added": result[10]
                        },
                        "message": "File succesfully retrieved"
                    }
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

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
        try:
            attachment = models.Attachment(emp_number, self.screen)
            return {
                "data": attachment.post(data),
                "message": "File succesfully created"
            }
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

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
        try:
            if attachment.put_comment(data) == 0:
                return {
                    "message": "Comment not updated, no change found on submitted data or no file_id found"
                }
            else:
                result = {
                    "file_id": data['file_id'],
                    "comment": data['comment'],
                    "message": "Comment succesfully updated"
                }
                return result
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def delete(self):
        emp_number = get_raw_jwt()['identity']
        parser = reqparse.RequestParser()
        parser.add_argument(
            'file_id', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        attachment = models.Attachment(emp_number, self.screen)
        try:
            if attachment.delete(data['file_id']) == 0:
                return {
                    "message": "No file_id found"
                }, 400
            else:
                result = {
                    "data": {
                        "file_id": data['file_id']
                    },
                    "message": "File succesfully deleted"
                }
                return result
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class PersonalDetailAttachment(Attachment):
    def __init__(self):
        self.screen = "personal"


class Nationality(Resource):
    def get(self):
        try:
            nationality = models.Nationality()
            result = []
            for nationality in nationality.get_all():
                result.append(
                    {
                        "nation_code": str(nationality[0]),
                        "nation_name": nationality[1]
                    }
                )
            return {
                "data": result,
                "message": "Nationality successfully retrieved"
            }
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class WorkShift(Resource):
    def get(self):
        try:
            workshift = models.WorkShift()
            result = []
            for workshift in workshift.get_all():
                result.append(
                    {
                        "workshift_code": str(workshift[0]),
                        "workshift_name": workshift[1]
                    }
                )
            return {
                "data": result,
                "message": "Workshift successfully retrieved"
            }
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class Religion(Resource):
    def get(self):
        try:
            religion = models.Religion()
            result = []
            for religion in religion.get_all():
                result.append(
                    {
                        "religion_code": str(religion[0]),
                        "religion_name": religion[1]
                    }
                )
            return {
                "data": result,
                "message": "Religion successfully retrieved"
            }
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500
