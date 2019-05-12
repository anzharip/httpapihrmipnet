import db
import bcrypt

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        field = "`emp_number`, `user_name`, `user_password`"
        table = "`ohrm_user`"
        sql_filter = "`user_name` = '%s'" % self.username
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1" % (
            field, table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchone()
        db.close_connection(connection, cursor)
        if result is None:
            return {
                "message": "User not found"
            }
        bytes_password = bytes(self.password, "utf-8")
        bytes_hashed = bytes(result[2], "utf-8")
        if bcrypt.checkpw(bytes_password, bytes_hashed):
            return {
                "message": "User & Password match"
            }
        else:
            return {
                "message": "User or Password is wrong"
            }

class PersonalDetail:
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.columns = "A.`emp_firstname`, A.`emp_middle_name`, A.`emp_lastname`, A.`employee_id`, A.`emp_other_id`, A.`emp_dri_lice_num`, A.`emp_dri_lice_exp_date`, A.`emp_bpjs_no`, A.`emp_npwp_no`, A.`emp_bpjs_ket_no`, D.`name` AS `work_shift_id`, A.`emp_gender`, A.`emp_marital_status`, E.`name` AS `nation_code`, A.`emp_birthday`, B.`name` AS `emp_religion`, A.`emp_birth_place`"
        self.table = "(((`hs_hr_employee` AS A JOIN `ohrm_religion` AS B ON A.`emp_religion`=B.`id`) JOIN `ohrm_employee_work_shift` AS C ON A.`emp_number`=C.`emp_number`) JOIN `ohrm_work_shift` AS D ON C.`work_shift_id`=D.`id`) JOIN `ohrm_nationality` AS E ON A.`nation_code`=E.`id`"

    def get(self):
        sql_filter = "`employee_id` LIKE %s" % self.employee_id
        statement = "SELECT %s FROM %s WHERE %s LIMIT 0,1000" % (
            self.columns, self.table, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        result = cursor.fetchall()
        db.close_connection(connection, cursor)
        result = {
            "first_name": result[0][0],
            "middle_name": result[0][1],
            "last_name": result[0][2],
            "employee_id": result[0][3],
            "no_ktp": result[0][4],
            "drivers_license_number": result[0][5],
            "license_expiry_date": result[0][6].isoformat(),
            "no_bpjs_kesehatan": result[0][7],
            "no_npwp": result[0][8],
            "no_bpjs_ketenagakerjaan": result[0][9],
            "work_shift": result[0][10],
            "gender": result[0][11],
            "marital_status": result[0][12],
            "nationality": result[0][13],
            "date_of_birth": result[0][14].isoformat(),
            "religion": result[0][15],
            "place_of_birth": result[0][16]
        }
        return result

    def put(self, body):
        table = "`hs_hr_employee` AS A JOIN `ohrm_employee_work_shift` AS B ON A.`emp_number` = B.`emp_number`"
        field = "A.`emp_firstname`='%s', A.`emp_middle_name`='%s', A.`emp_lastname`='%s', A.`emp_other_id`='%s', A.`emp_dri_lice_exp_date`='%s', A.`emp_bpjs_no`='%s', A.`emp_npwp_no`='%s', A.`emp_bpjs_ket_no`='%s', B.`work_shift_id`='%s', A.`emp_gender`='%s', A.`emp_marital_status`='%s', A.`nation_code`='%s', A.`emp_religion`='%s', A.`emp_birth_place`='%s'" % (
            body["first_name"], body["middle_name"], body["last_name"], body["no_ktp"], body["license_expiry_date"], body["no_bpjs_kesehatan"], body["no_npwp"], body["no_bpjs_ketenagakerjaan"], body["work_shift"], body["gender"], body["marital_status"], body["nationality"], body["religion"], body["place_of_birth"])
        sql_filter = "`employee_id` = '%s'" % (self.employee_id)
        statement = "UPDATE %s SET %s WHERE %s " % (
            table, field, sql_filter)
        connection = db.open_connection()
        cursor = db.sql_cursor(connection, statement)
        connection.commit()
        db.close_connection(cursor, connection)
        result = {
            "message": "Personal detail succesfully updated"
        }
        return result
