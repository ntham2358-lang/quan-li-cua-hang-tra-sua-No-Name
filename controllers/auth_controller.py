from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash

MAX_FAILED_ATTEMPTS = 5
LOCK_DURATION_MINUTES = 15


class AuthController:
    def __init__(self, model):
        self.model = model

    def login(self, username: str, password: str):
        user = self.model.get_user_by_username(username.strip())
        if not user:
            return False, "Sai tên đăng nhập hoặc mật khẩu."

        now = datetime.now()
        if user["status"] == "Locked" and user["locked_until"] and now < user["locked_until"]:
            return False, "Tài khoản đang bị khóa tạm thời trong 15 phút do nhập sai quá 5 lần."

        if user["status"] == "Inactive" or user["staff_status"] == "Đã nghỉ việc":
            return False, "Tài khoản đã ngừng hoạt động."

        if not check_password_hash(user["password_hash"], password):
            failed = user["failed_attempts"] + 1
            new_status = "Locked" if failed >= MAX_FAILED_ATTEMPTS else user["status"]
            locked_until = now + timedelta(minutes=LOCK_DURATION_MINUTES) if failed >= MAX_FAILED_ATTEMPTS else None
            self.model.update_login_failure(user["user_id"], failed, new_status, locked_until)
            return False, f"Sai mật khẩu (số lần sai liên tiếp: {failed}/{MAX_FAILED_ATTEMPTS})."

        self.model.update_login_success(user["user_id"], now)
        return True, {
            "user_id": user["user_id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "role": user["role_name"],
            "staff_id": user["staff_id"],
        }

    def change_password(self, user_id: int, username: str, old_password: str, new_password: str, confirm_password: str):
        if new_password != confirm_password:
            return False, "Mật khẩu mới và xác nhận mật khẩu không khớp."
        if len(new_password) < 8:
            return False, "Mật khẩu mới phải có ít nhất 8 ký tự."

        user = self.model.get_user_by_username(username)
        if not user or user["user_id"] != user_id:
            return False, "Không tìm thấy tài khoản."
        if not check_password_hash(user["password_hash"], old_password):
            return False, "Mật khẩu hiện tại không đúng."

        self.model.update_password_hash(user_id, generate_password_hash(new_password))
        return True, "Đổi mật khẩu thành công. Vui lòng đăng nhập lại."

    def create_staff_account(self, actor_role: str, staff_id: int, role_name: str, username: str, raw_password: str):
        if actor_role not in ("Owner", "Manager"):
            return False, "Chỉ Chủ cửa hàng hoặc Quản lý mới được tạo tài khoản."

        staff = self.model.get_staff_by_id(staff_id)
        if not staff or staff["status"] != "Đang làm việc":
            return False, "Nhân viên không tồn tại hoặc không ở trạng thái Đang làm việc."
        if self.model.staff_has_user(staff_id):
            return False, "Nhân viên này đã được cấp tài khoản."
        if self.model.get_user_by_username(username.strip()):
            return False, "Tên đăng nhập đã tồn tại."

        role = self.model.get_role_by_name(role_name)
        if not role:
            return False, "Vai trò không hợp lệ."

        user_id = self.model.create_user(
            staff_id=staff_id,
            role_id=role["role_id"],
            username=username.strip(),
            password_hash=generate_password_hash(raw_password),
        )
        return True, f"Tạo tài khoản thành công (user_id={user_id})."

    def toggle_status(self, actor_user_id: int, actor_role: str, target_username: str, new_status: str):
        if actor_role not in ("Owner", "Manager"):
            return False, "Không có quyền khóa/mở khóa tài khoản."
        if new_status not in ("Active", "Inactive", "Locked"):
            return False, "Trạng thái không hợp lệ."

        target = self.model.get_user_by_username(target_username)
        if not target:
            return False, "Không tìm thấy tài khoản mục tiêu."
        if target["user_id"] == actor_user_id:
            return False, "Không thể tự khóa tài khoản của chính mình."

        self.model.update_user_status(target["user_id"], new_status)
        return True, f"Đã cập nhật trạng thái tài khoản '{target_username}' -> {new_status}."

    def assign_role(self, actor_role: str, target_username: str, new_role_name: str):
        if actor_role not in ("Owner", "Manager"):
            return False, "Không có quyền phân quyền."
        if new_role_name == "Owner" and actor_role != "Owner":
            return False, "Chỉ Chủ cửa hàng (Owner) mới được cấp quyền Owner."

        target = self.model.get_user_by_username(target_username)
        if not target:
            return False, "Không tìm thấy tài khoản mục tiêu."
        role = self.model.get_role_by_name(new_role_name)
        if not role:
            return False, "Vai trò không tồn tại."

        self.model.update_user_role(target["user_id"], role["role_id"])
        return True, f"Đã gán vai trò '{new_role_name}' cho '{target_username}'."