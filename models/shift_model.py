from .db_connection import get_connection
from datetime import datetime

class ShiftModel:
    def get_all_shifts(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM shifts ORDER BY shift_id")
                return cur.fetchall()

    def assign_shift(self, staff_id, shift_id, work_date):
        sql = "INSERT INTO shift_assignments (staff_id, shift_id, work_date) VALUES (%s, %s, %s) RETURNING assignment_id"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (staff_id, shift_id, work_date))
                assign_id = cur.fetchone()["assignment_id"]
            conn.commit()
        return assign_id

    def check_in(self, staff_id, shift_id, work_date):
        now = datetime.now()
        sql = "INSERT INTO attendance (staff_id, shift_id, work_date, check_in) VALUES (%s, %s, %s, %s)"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (staff_id, shift_id, work_date, now))
            conn.commit()

    def check_out(self, staff_id, shift_id, work_date):
        now = datetime.now()
        sql = "UPDATE attendance SET check_out = %s WHERE staff_id = %s AND shift_id = %s AND work_date = %s AND check_out IS NULL"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (now, staff_id, shift_id, work_date))
                rows_affected = cur.rowcount
            conn.commit()
        return rows_affected > 0