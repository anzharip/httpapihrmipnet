from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import models
from base64 import b64encode
from aesb64 import encrypt

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
        except:
            return {'message': 'Something went wrong'}, 500


class PersonalDetail(Resource):
    @jwt_required
    def get(self):
        emp_number = get_raw_jwt()['identity']
        try:
            personal_detail = models.PersonalDetail(emp_number)
            return personal_detail.get()
        except:
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
            return personal_detail.put(data)
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
            'file_id', help='This field cannot be blank', required=True, location='args')
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
                    }, 400
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
        except:
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
            return attachment.post(data)
        except:
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
                    "message": "Comment not updated or no file_id found"
                }
            else:
                result = {
                    "file_id": data['file_id'],
                    "comment": data['comment'],
                    "message": "Comment succesfully updated"
                }
                return result
        except:
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
                    "file_id": data['file_id'],
                    "message": "File succesfully deleted"
                }
                return result
        except:
            return {'message': 'Something went wrong'}, 500

class PersonalDetailAttachment(Attachment):
    def __init__(self):
        self.screen = "personal"

class ContactDetailAttachment(Attachment):
    def __init__(self):
        self.screen = "contact"


class EmergencyContact(Resource):
    @jwt_required
    def get(self):
        emp_number = get_raw_jwt()['identity']
        emergency_contact = models.EmergencyContact(emp_number)
        parser = reqparse.RequestParser()
        parser.add_argument(
            'emergencycontact_id', help='This field cannot be blank', required=True, location='args')
        data = parser.parse_args()
        try:
            if data["emergencycontact_id"] == "all":
                result = []
                for emergency_contact in emergency_contact.get_all():
                    result.append(
                        {
                            "emergencycontact_id": str(emergency_contact[1]),
                            "name": emergency_contact[2],
                            "relationship": emergency_contact[3],
                            "mobile": emergency_contact[5],
                            "home_telephone": emergency_contact[4],
                            "work_telephone": emergency_contact[6],
                            "address": emergency_contact[7],
                            "message": "Emergency contact succesfully retrieved"
                        }
                    )
                return result
            else:
                result = emergency_contact.get(data["emergencycontact_id"])
                if result is None:
                    return {
                        "message": "Emergency Contact not found"
                    }, 400
                else:
                    return {
                        "emergencycontact_id": str(result[1]),
                        "name": result[2],
                        "relationship": result[3],
                        "mobile": result[5],
                        "home_telephone": result[4],
                        "work_telephone": result[6],
                        "address": result[7],
                        "message": "Emergency contact succesfully retrieved"
                    }
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def post(self):
        emp_number = get_raw_jwt()['identity']
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name', help='This field cannot be blank', required=True)
        parser.add_argument(
            'relationship', help='This field cannot be blank', required=True)
        parser.add_argument(
            'mobile', help='This field cannot be blank', required=True)
        parser.add_argument(
            'home_telephone', help='This field cannot be blank', required=True)
        parser.add_argument(
            'work_telephone', help='This field cannot be blank', required=True)
        parser.add_argument(
            'address', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        try:
            emergency_contact = models.EmergencyContact(emp_number)
            return emergency_contact.post(data)
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def put(self):
        emp_number = get_raw_jwt()['identity']
        parser = reqparse.RequestParser()
        parser.add_argument(
            'emergencycontact_id', help='This field cannot be blank', required=True)
        parser.add_argument(
            'name', help='This field cannot be blank', required=True)
        parser.add_argument(
            'relationship', help='This field cannot be blank', required=True)
        parser.add_argument(
            'mobile', help='This field cannot be blank', required=True)
        parser.add_argument(
            'home_telephone', help='This field cannot be blank', required=True)
        parser.add_argument(
            'work_telephone', help='This field cannot be blank', required=True)
        parser.add_argument(
            'address', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        emergency_contact = models.EmergencyContact(emp_number)
        try:
            if emergency_contact.put(data) == 0:
                return {
                    "message": "Emergency Contact not updated or no emergencycontact_id found"
                }, 400
            else:
                result = {
                    "emergencycontact_id": data["emergencycontact_id"],
                    "name": data["name"],
                    "relationship": data["relationship"],
                    "mobile": data["mobile"],
                    "home_telephone": data["home_telephone"],
                    "work_telephone": data["work_telephone"],
                    "address": data["address"],
                    "message": "Emergency Contact succesfully updated"
                }
                return result
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def delete(self):
        emp_number = get_raw_jwt()['identity']
        parser = reqparse.RequestParser()
        parser.add_argument(
            'emergencycontact_id', help='This field cannot be blank', required=True, location='args')
        data = parser.parse_args()
        emergency_contact = models.EmergencyContact(emp_number)
        try:
            if emergency_contact.delete(data['emergencycontact_id']) == 0:
                return {
                    "message": "No emergencycontact_id found"
                }, 400
            else:
                result = {
                    "emergencycontact_id": data['emergencycontact_id'],
                    "message": "Emergency Contact succesfully deleted"
                }
                return result
        except:
            return {'message': 'Something went wrong'}, 500


class EmergencyContactAttachment(Attachment):
    def __init__(self):
        self.screen = "emergency"


class DependentAttachment(Attachment):
    def __init__(self):
        self.screen = "dependent"


class ContactDetail(Resource):
    @jwt_required
    def get(self):
        emp_number = get_raw_jwt()['identity']
        contact_detail = models.ContactDetail(emp_number)
        try:
            data = contact_detail.get()
            return {
                "address_street_1": data[1],
                "address_street_2": data[2],
                "city": data[3],
                "state_province": data[4],
                "zip_postal_code": data[5],
                "country": data[6],
                "home_telephone": data[7],
                "mobile": data[8],
                "work_telephone": data[9],
                "work_email": data[10],
                "other_email": data[11],
                "message": "Contact detail retrieved succesfully"
            }
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'address_street_1', help='This field cannot be blank', required=True)
        parser.add_argument(
            'address_street_2', help='This field cannot be blank', required=True)
        parser.add_argument(
            'city', help='This field cannot be blank', required=True)
        parser.add_argument(
            'state_province', help='This field cannot be blank', required=True)
        parser.add_argument(
            'zip_postal_code', help='This field cannot be blank', required=True)
        parser.add_argument(
            'country', help='This field cannot be blank', required=True)
        parser.add_argument(
            'home_telephone', help='This field cannot be blank', required=True)
        parser.add_argument(
            'mobile', help='This field cannot be blank', required=True)
        parser.add_argument(
            'work_telephone', help='This field cannot be blank', required=True)
        parser.add_argument(
            'work_email', help='This field cannot be blank', required=True)
        parser.add_argument(
            'other_email', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        emp_number = get_raw_jwt()['identity']
        contact_detail = models.ContactDetail(emp_number)
        try:
            result = contact_detail.put(data)
            if result == 0:
                return {
                    "message": "Contact detail not updated"
                }, 400
            else:
                return {
                    "message": "Contact detail successfully updated"
                }
        except:
            return {'message': 'Something went wrong'}, 500


class Dependent(Resource):
    @jwt_required
    def get(self):
        emp_number = get_raw_jwt()['identity']
        dependent = models.Dependent(emp_number)
        parser = reqparse.RequestParser()
        parser.add_argument(
            'dependent_id', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        try:
            if data["dependent_id"] == "all":
                result = []
                for dependent in dependent.get_all():
                    result.append(
                        {
                            "dependent_id": str(dependent[1]),
                            "name": dependent[2],
                            "relationship": dependent[3],
                            "gender": str(dependent[6]),
                            "date_of_birth": dependent[5].isoformat(),
                            "message": "Dependent succesfully retrieved"
                        }
                    )
                return result
            else:
                result = dependent.get(data["dependent_id"])
                if result is None:
                    return {
                        "message": "Dependent not found"
                    }, 400
                else:
                    return {
                        "dependent_id": str(result[1]),
                        "name": result[2],
                        "relationship": result[3],
                        "gender": result[6],
                        "date_of_birth": result[5].isoformat(),
                        "message": "Dependent succesfully retrieved"
                    }
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def post(self):
        emp_number = get_raw_jwt()['identity']
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name', help='This field cannot be blank', required=True)
        parser.add_argument(
            'relationship', help='This field cannot be blank', required=True)
        parser.add_argument(
            'gender', help='This field cannot be blank', required=True)
        parser.add_argument(
            'date_of_birth', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        try:
            dependent = models.Dependent(emp_number)
            return dependent.post(data)
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def put(self):
        emp_number = get_raw_jwt()['identity']
        parser = reqparse.RequestParser()
        parser.add_argument(
            'dependent_id', help='This field cannot be blank', required=True)
        parser.add_argument(
            'name', help='This field cannot be blank', required=True)
        parser.add_argument(
            'relationship', help='This field cannot be blank', required=True)
        parser.add_argument(
            'gender', help='This field cannot be blank', required=True)
        parser.add_argument(
            'date_of_birth', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        dependent = models.Dependent(emp_number)
        try:
            if dependent.put(data) == 0:
                return {
                    "message": "Dependent not updated or no dependent_id found"
                }, 400
            else:
                result = {
                    "dependent_id": str(data["dependent_id"]),
                    "name": data["name"],
                    "relationship": data["relationship"],
                    "gender": str(data["gender"]),
                    "date_of_birth": data["date_of_birth"],
                    "message": "Dependent succesfully updated"
                }
                return result
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def delete(self):
        emp_number = get_raw_jwt()['identity']
        parser = reqparse.RequestParser()
        parser.add_argument(
            'dependent_id', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        dependent = models.Dependent(emp_number)
        try:
            if dependent.delete(data['dependent_id']) == 0:
                return {
                    "message": "No dependent_id found"
                }, 400
            else:
                result = {
                    "dependent_id": str(data['dependent_id']),
                    "message": "Dependent succesfully deleted"
                }
                return result
        except:
            return {'message': 'Something went wrong'}, 500


class Job(Resource):
    @jwt_required
    def get(self):
        emp_number = get_raw_jwt()['identity']
        try:
            job = models.Job(emp_number)
            return job.get()
        except:
            return {'message': 'Something went wrong'}, 500


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
            return result
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
            return result
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
            return result
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class Country(Resource):
    def get(self):
        try:
            country = models.Country()
            result = []
            for country in country.get_all():
                result.append(
                    {
                        "country_code": country[0],
                        "country_name": country[1]
                    }
                )
            return result
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500
