import db
import bcrypt
from time import time
from mimetypes import guess_type
from base64 import b64decode
import datetime


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get(self):
        field = "`emp_number`, `user_name`, `user_password`"
        table = "`ohrm_user`"
        sql_filter = "`user_name` = '%s'" % self.username
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchone()
        db.close_connection(connection, cursor)
        return result

    def verify_hash(self):
        field = "`emp_number`, `user_name`, `user_password`"
        table = "`ohrm_user`"
        sql_filter = "`user_name` = '%s'" % self.username
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchone()
        db.close_connection(connection, cursor)
        bytes_password = bytes(self.password, "utf-8")
        bytes_hashed = bytes(result[2], "utf-8")
        return bcrypt.checkpw(bytes_password, bytes_hashed)


class PersonalDetail:
    def __init__(self, emp_number):
        self.emp_number = emp_number

    def get(self):
        field = "A.`emp_firstname`, A.`emp_middle_name`, A.`emp_lastname`, A.`employee_id`, A.`emp_other_id`, A.`emp_dri_lice_num`, A.`emp_dri_lice_exp_date`, A.`emp_bpjs_no`, A.`emp_npwp_no`, A.`emp_bpjs_ket_no`, D.`id` AS `work_shift_id`, A.`emp_gender`, A.`emp_marital_status`, E.`id` AS `nation_code`, A.`emp_birthday`, B.`id` AS `emp_religion`, A.`emp_birth_place`"
        table = "(((`hs_hr_employee` AS A JOIN `ohrm_religion` AS B ON A.`emp_religion`=B.`id`) JOIN `ohrm_employee_work_shift` AS C ON A.`emp_number`=C.`emp_number`) JOIN `ohrm_work_shift` AS D ON C.`work_shift_id`=D.`id`) JOIN `ohrm_nationality` AS E ON A.`nation_code`=E.`id`"
        sql_filter = "A.`emp_number` LIKE %s" % self.emp_number
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchone()
        db.close_connection(connection, cursor)
        if isinstance(result[6], datetime.datetime): 
            license_expiry_date = result[6].isoformat()
        else: 
            license_expiry_date = "" 
        result = {
            "first_name": result[0],
            "middle_name": result[1],
            "last_name": result[2],
            "employee_id": result[3],
            "no_ktp": result[4],
            "drivers_license_number": result[5],
            # "license_expiry_date": result[6].isoformat(),
            "license_expiry_date": license_expiry_date,
            "no_bpjs_kesehatan": result[7],
            "no_npwp": result[8],
            "no_bpjs_ketenagakerjaan": result[9],
            "work_shift": str(result[10]),
            "gender": str(result[11]),
            "marital_status": result[12],
            "nationality": str(result[13]),
            "date_of_birth": result[14].isoformat(),
            "religion": str(result[15]),
            "place_of_birth": result[16]
        }
        return result

    def put(self, body):
        table = "`hs_hr_employee` AS A JOIN `ohrm_employee_work_shift` AS B ON A.`emp_number` = B.`emp_number`"
        field = "A.`emp_firstname`='%s', A.`emp_middle_name`='%s', A.`emp_lastname`='%s', A.`emp_other_id`='%s', A.`emp_dri_lice_exp_date`='%s', A.`emp_bpjs_no`='%s', A.`emp_npwp_no`='%s', A.`emp_bpjs_ket_no`='%s', B.`work_shift_id`='%s', A.`emp_gender`='%s', A.`emp_marital_status`='%s', A.`nation_code`='%s', A.`emp_religion`='%s', A.`emp_birth_place`='%s'" % (
            body["first_name"], body["middle_name"], body["last_name"], body["no_ktp"], body["license_expiry_date"], body["no_bpjs_kesehatan"], body["no_npwp"], body["no_bpjs_ketenagakerjaan"], body["work_shift"], body["gender"], body["marital_status"], body["nationality"], body["religion"], body["place_of_birth"])
        sql_filter = "A.`emp_number` = '%s'" % (self.emp_number)
        statement = "UPDATE %s SET %s WHERE %s " % (
            table, field, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        connection.commit()
        db.close_connection(cursor, connection)
        result = cursor.rowcount
        return result


class Attachment:
    def __init__(self, emp_number, screen):
        self.emp_number = emp_number
        self.screen = screen

    def get_meta_all(self):
        field = "`emp_number`,`eattach_id`,`eattach_desc`,`eattach_filename`, `eattach_size`,`eattach_type`,`screen`,`attached_by`,`attached_by_name`, DATE_FORMAT(`attached_time`, '%Y-%m-%dT%T') AS `attached_time`"
        table = "`hs_hr_emp_attachment`"
        sql_filter = "`emp_number`='%s' AND `screen`='%s'" % (
            self.emp_number, self.screen)
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1000" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchall()
        db.close_connection(connection, cursor)
        return result

    def get_meta(self, file_id):
        field = "`emp_number`,`eattach_id`,`eattach_desc`, `eattach_filename`, `eattach_size`, `eattach_type`,`screen`,`attached_by`,`attached_by_name`, DATE_FORMAT(`attached_time`, '%Y-%m-%dT%T') AS `attached_time`"
        table = "`hs_hr_emp_attachment`"
        sql_filter = "`emp_number`='%s' AND `screen`='%s' AND `eattach_id` = '%s'" % (
            self.emp_number, self.screen, file_id)
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchone()
        db.close_connection(connection, cursor)
        return result

    def get(self, file_id):
        field = "`emp_number`,`eattach_id`,`eattach_desc`, `eattach_filename`, `eattach_size`, `eattach_attachment`, `eattach_type`,`screen`,`attached_by`,`attached_by_name`, DATE_FORMAT(`attached_time`, '%Y-%m-%dT%T') AS `attached_time`"
        table = "`hs_hr_emp_attachment`"
        sql_filter = "`emp_number`='%s' AND `screen`='%s' AND `eattach_id` = '%s'" % (
            self.emp_number, self.screen, file_id)
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchone()
        db.close_connection(connection, cursor)
        return result

    def put_comment(self, body):
        field = "`eattach_desc` = '%s'" % body['comment']
        table = "`hs_hr_emp_attachment`"
        sql_filter = "`emp_number`='%s' AND `screen`='%s' AND `eattach_id` = '%s'" % (
            self.emp_number, self.screen, body['file_id'])
        statement = "UPDATE %s SET %s WHERE %s" % (
            table, field, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        connection.commit()
        db.close_connection(connection, cursor)
        return cursor.rowcount

    def post(self, body):
        emp_number = self.emp_number
        eattach_id = str(int(time()))
        eattach_desc = body['comment']
        eattach_filename = body['file_name']
        eattach_attachment = b64decode(body["select_file"]).hex()
        eattach_size = int((len(body["select_file"]) * 3/4) -
                           body["select_file"].count("=", -2))
        eattach_size = str(eattach_size)
        eattach_type = guess_type(eattach_filename)[0]
        screen = self.screen
        attached_by = self.emp_number
        field = "(`emp_number`,`eattach_id`,`eattach_desc`, `eattach_filename`, `eattach_size`, `eattach_attachment`, `eattach_type`,`screen`,`attached_by`)"
        values = "('%s', '%s', '%s', '%s', '%s', x'%s', '%s', '%s', '%s')" % (emp_number, eattach_id, eattach_desc,
                                                                              eattach_filename, eattach_size, eattach_attachment, eattach_type, screen, attached_by)
        table = "`hs_hr_emp_attachment`"
        statement = "INSERT INTO %s %s VALUES %s" % (
            table, field, values)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        connection.commit()
        db.close_connection(connection, cursor)
        result = {
            "file_id": eattach_id,
            "comment": eattach_desc,
            "file_name": eattach_filename,
            "size": eattach_size,
            "type": eattach_type,
            "date_added": self.get_meta(eattach_id)[9]
        }
        return result

    def delete(self, file_id):
        table = "`hs_hr_emp_attachment`"
        sql_filter = "`emp_number` = %s AND `eattach_id` = %s" % (
            self.emp_number, file_id)
        statement = "DELETE FROM %s WHERE %s" % (
            table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        connection.commit()
        db.close_connection(connection, cursor)
        return cursor.rowcount


class ContactDetail:
    def __init__(self, emp_number):
        self.emp_number = emp_number

    def get(self):
        field = "`emp_number`,`emp_street1`,`emp_street2`,`city_code`,`provin_code`,`emp_zipcode`,`coun_code`,`emp_hm_telephone`,`emp_mobile`,`emp_work_telephone`,`emp_work_email`,`emp_oth_email`"
        table = "`hs_hr_employee`"
        sql_filter = "`emp_number` = %s" % self.emp_number
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchone()
        db.close_connection(connection, cursor)
        return result

    def put(self, body):
        table = "`hs_hr_employee`"
        field = "`emp_street1` = '%s',`emp_street2` = '%s',`city_code` = '%s',`provin_code` = '%s',`emp_zipcode` = '%s', `coun_code` = '%s', `emp_hm_telephone` = '%s', `emp_mobile` = '%s', `emp_work_telephone` = '%s', `emp_work_email` = '%s', `emp_oth_email` = '%s'" % (
            body["address_street_1"], body["address_street_2"], body["city"], body["state_province"], body["zip_postal_code"], body[
                "country"], body["home_telephone"], body["mobile"], body["work_telephone"], body["work_email"], body["other_email"]
        )
        sql_filter = "`emp_number` = '%s'" % (self.emp_number)
        statement = "UPDATE %s SET %s WHERE %s " % (
            table, field, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        connection.commit()
        db.close_connection(cursor, connection)
        return cursor.rowcount


class EmergencyContact:
    def __init__(self, emp_number):
        self.emp_number = emp_number

    def get_all(self):
        field = "`emp_number`,`eec_seqno`,`eec_name`,`eec_relationship`,`eec_home_no`,`eec_mobile_no`,`eec_office_no`,`eec_address`"
        table = "`hs_hr_emp_emergency_contacts`"
        sql_filter = "`emp_number`='%s'" % (
            self.emp_number)
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1000" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchall()
        db.close_connection(connection, cursor)
        return result

    def get(self, eec_seqno):
        field = "`emp_number`,`eec_seqno`,`eec_name`,`eec_relationship`,`eec_home_no`,`eec_mobile_no`,`eec_office_no`,`eec_address`"
        table = "`hs_hr_emp_emergency_contacts`"
        sql_filter = "`emp_number`='%s'  AND `eec_seqno` = '%s'" % (
            self.emp_number, eec_seqno)
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchone()
        db.close_connection(connection, cursor)
        return result

    def get_next_eec_seqno_value(self):
        field = "`eec_seqno`"
        table = "`hs_hr_emp_emergency_contacts`"
        sql_filter = "`emp_number`='%s'" % (
            self.emp_number)
        statement = "SELECT %s FROM %s WHERE %s ORDER BY `eec_seqno` DESC LIMIT 0,1" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchone()
        db.close_connection(connection, cursor)
        if result is None:
            return "1"
        else:
            return str(result[0]+1)

    def post(self, body):
        eec_seqno = self.get_next_eec_seqno_value()
        field = "(`emp_number`, `eec_seqno`, `eec_name`, `eec_relationship`, `eec_home_no`, `eec_mobile_no`, `eec_office_no`, `eec_address`)"
        values = "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (self.emp_number, eec_seqno,
                                                                       body["name"], body["relationship"], body["home_telephone"], body["mobile"], body["work_telephone"], body["address"])
        table = "`hs_hr_emp_emergency_contacts`"
        statement = "INSERT INTO %s %s VALUES %s" % (
            table, field, values)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        connection.commit()
        db.close_connection(connection, cursor)
        result = {
            "emergency_contactid": eec_seqno,
            "name": body["name"],
            "relationship": body["relationship"],
            "mobile": body["mobile"],
            "home_telephone": body["home_telephone"],
            "work_telephone": body["work_telephone"],
            "address": body["address"]
        }
        return result

    def put(self, body):
        field = "`eec_name` = '%s', `eec_relationship` = '%s', `eec_home_no` = '%s', `eec_mobile_no` = '%s', `eec_office_no` = '%s', `eec_address` = '%s'" % (
            body["name"], body["relationship"], body["home_telephone"], body["mobile"], body["work_telephone"], body["address"])
        table = "`hs_hr_emp_emergency_contacts`"
        sql_filter = "`emp_number`='%s' AND `eec_seqno` = '%s'" % (
            self.emp_number, body["emergencycontact_id"])
        statement = "UPDATE %s SET %s WHERE %s" % (
            table, field, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        connection.commit()
        db.close_connection(connection, cursor)
        return cursor.rowcount

    def delete(self, emergencycontact_id):
        table = "`hs_hr_emp_emergency_contacts`"
        sql_filter = "`emp_number`='%s' AND `eec_seqno` = '%s'" % (
            self.emp_number, emergencycontact_id)
        statement = "DELETE FROM %s WHERE %s" % (
            table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        connection.commit()
        db.close_connection(connection, cursor)
        return cursor.rowcount


class Dependent:
    def __init__(self, emp_number):
        self.emp_number = emp_number

    def get_all(self):
        field = "`emp_number`, `ed_seqno`, `ed_name`, `ed_relationship_type`, `ed_relationship`, `ed_date_of_birth`, `ed_gender`"
        table = "`hs_hr_emp_dependents`"
        sql_filter = "`emp_number`='%s'" % (
            self.emp_number)
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1000" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchall()
        db.close_connection(connection, cursor)
        return result

    def get(self, ed_seqno):
        field = "`emp_number`, `ed_seqno`, `ed_name`, `ed_relationship_type`, `ed_relationship`, `ed_date_of_birth`, `ed_gender`"
        table = "`hs_hr_emp_dependents`"
        sql_filter = "`emp_number`='%s'  AND `ed_seqno` = '%s'" % (
            self.emp_number, ed_seqno)
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchone()
        db.close_connection(connection, cursor)
        return result

    def get_next_ed_seqno_value(self):
        field = "`ed_seqno`"
        table = "`hs_hr_emp_dependents`"
        sql_filter = "`emp_number`='%s'" % (
            self.emp_number)
        statement = "SELECT %s FROM %s WHERE %s ORDER BY `ed_seqno` DESC LIMIT 0,1" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchone()
        db.close_connection(connection, cursor)
        if result is None:
            return "1"
        else:
            return str(result[0]+1)

    def post(self, body):
        ed_seqno = self.get_next_ed_seqno_value()
        field = "(`emp_number`, `ed_seqno`, `ed_name`, `ed_relationship_type`, `ed_gender`, `ed_date_of_birth`)"
        values = "('%s', '%s', '%s', '%s', '%s', '%s')" % (self.emp_number, ed_seqno,
                                                           body["name"], body["relationship"], body["gender"], body["date_of_birth"])
        table = "`hs_hr_emp_dependents`"
        statement = "INSERT INTO %s %s VALUES %s" % (
            table, field, values)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        connection.commit()
        db.close_connection(connection, cursor)
        result = {
            "dependent_id": ed_seqno,
            "name": body["name"],
            "relationship": body["relationship"],
            "gender": body["gender"],
            "date_of_birth": body["date_of_birth"]
        }
        return result

    def put(self, body):
        field = "`ed_name` = '%s', `ed_relationship_type` = '%s', `ed_gender` = '%s', `ed_date_of_birth` = '%s'" % (
            body["name"], body["relationship"], body["gender"], body["date_of_birth"])
        table = "`hs_hr_emp_dependents`"
        sql_filter = "`emp_number`='%s' AND `ed_seqno` = '%s'" % (
            self.emp_number, body["dependent_id"])
        statement = "UPDATE %s SET %s WHERE %s" % (
            table, field, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        connection.commit()
        db.close_connection(connection, cursor)
        return cursor.rowcount

    def delete(self, dependent_id):
        table = "`hs_hr_emp_dependents`"
        sql_filter = "`emp_number`='%s' AND `ed_seqno` = '%s'" % (
            self.emp_number, dependent_id)
        statement = "DELETE FROM %s WHERE %s" % (
            table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        connection.commit()
        db.close_connection(connection, cursor)
        return cursor.rowcount


class Job:
    def __init__(self, emp_number):
        self.emp_number = emp_number

    def get(self):
        field = "A.`emp_number`,C.`job_title` AS `job_title_code`,DATE_FORMAT(A.`joined_date`,'%Y-%m-%d') AS `joined_date`,D.`name` AS `work_station`,E.`name` AS `location_id`,A.`att_type`,DATE_FORMAT(A.`resign_date`,'%Y-%m-%d') AS `resign_date`"
        table = "(((`hs_hr_employee` AS A JOIN `hs_hr_emp_locations` AS B ON A.`emp_number`=B.`emp_number`) JOIN `ohrm_job_title` AS C ON A.`job_title_code`=C.`id`) JOIN `ohrm_subunit` AS D ON A.`work_station`=D.`id`) JOIN `ohrm_location` AS E ON B.`location_id`=E.`id`"
        sql_filter = "A.`emp_number`='%s'" % (
            self.emp_number)
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchone()
        db.close_connection(connection, cursor)
        return {
            "job_title": result[1],
            "joined_date": result[2],
            "department": result[3],
            "location": result[4],
            "attendance_type": result[5],
            "resign_date": result[6]
        }


class Nationality():
    def get_all(self):
        field = "`id`, `name`"
        table = "`ohrm_nationality`"
        statement = "SELECT %s FROM %s LIMIT 0,1000" % (
            field, table)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchall()
        db.close_connection(connection, cursor)
        return result


class WorkShift():
    def get_all(self):
        field = "`id`, `name`"
        table = "`ohrm_work_shift`"
        statement = "SELECT %s FROM %s LIMIT 0,1000" % (
            field, table)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchall()
        db.close_connection(connection, cursor)
        return result


class Religion():
    def get_all(self):
        field = "`id`, `name`"
        table = "`ohrm_religion`"
        statement = "SELECT %s FROM %s LIMIT 0,1000" % (
            field, table)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchall()
        db.close_connection(connection, cursor)
        return result


class Country():
    def get_all(self):
        field = "`cou_code`, `cou_name`"
        table = "`hs_hr_country`"
        statement = "SELECT %s FROM %s LIMIT 0,1000" % (
            field, table)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchall()
        db.close_connection(connection, cursor)
        return result
