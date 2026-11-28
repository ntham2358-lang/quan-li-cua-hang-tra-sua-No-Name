from .db_connection import get_connection


class AuthUserModel:
    def get_user_by_username(self, username: str):
        sql = """
            SELECT u.*, r.role_name, s.full_name, s.status AS staff_status, s.email
            FROM users u
            JOIN roles r ON u.role_id = r.role_id
            JOIN staff s ON u.staff_id = s.staff_id
            WHERE u.username = %s
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username,))
                return cur.fetchone()

    def get_role_by_name(self, role_name: str):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM roles WHERE role_name = %s", (role_name,))
                return cur.fetchone()

    def get_staff_by_id(self, staff_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM staff WHERE staff_id = %s", (staff_id,))
                return cur.fetchone()

    def staff_has_user(self, staff_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM users WHERE staff_id = %s", (staff_id,))
                return cur.fetchone() is not None

    def create_user(self, staff_id: int, role_id: int, username: str, password_hash: str) -> int:
        sql = """
            INSERT INTO users (staff_id, role_id, username, password_hash, status)
            VALUES (%s, %s, %s, %s, 'Active')
            RETURNING user_id
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (staff_id, role_id, username, password_hash))
                user_id = cur.fetchone()["user_id"]
            conn.commit()
        return user_id

    def update_login_failure(self, user_id: int, failed_attempts: int, status: str, locked_until):
        sql = """
            UPDATE users
            SET failed_attempts = %s, status = %s, locked_until = %s
            WHERE user_id = %s
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (failed_attempts, status, locked_until, user_id))
            conn.commit()

    def update_login_success(self, user_id: int, last_login):
        sql = """
            UPDATE users
            SET failed_attempts = 0, status = 'Active', locked_until = NULL, last_login = %s
            WHERE user_id = %s
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (last_login, user_id))
            conn.commit()

    def update_password_hash(self, user_id: int, new_hash: str):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET password_hash = %s WHERE user_id = %s", (new_hash, user_id))
            conn.commit()

    def update_user_status(self, user_id: int, status: str):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET status = %s WHERE user_id = %s", (status, user_id))
            conn.commit()

    def update_user_role(self, user_id: int, role_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET role_id = %s WHERE user_id = %s", (role_id, user_id))
            conn.commit()