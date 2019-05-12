import db


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
