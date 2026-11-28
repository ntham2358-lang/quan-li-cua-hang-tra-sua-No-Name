class ShiftController:
    def __init__(self, model):
        self.model = model

    def assign_shift(self, actor_role, staff_id, shift_id, work_date):
        if actor_role not in ("Owner", "Manager"):
            return False, "Chỉ Quản lý mới được phân ca."
        try:
            assign_id = self.model.assign_shift(staff_id, shift_id, work_date)
            return True, f"Phân ca thành công (ID: {assign_id})."
        except Exception as e:
            return False, f"Lỗi phân ca (có thể đã phân rồi): {e}"

    def check_in(self, staff_id, shift_id, work_date):
        try:
            self.model.check_in(staff_id, shift_id, work_date)
            return True, "Check-in thành công."
        except Exception as e:
            return False, f"Lỗi check-in: {e}"

    def check_out(self, staff_id, shift_id, work_date):
        success = self.model.check_out(staff_id, shift_id, work_date)
        if success:
            return True, "Check-out thành công."
        return False, "Không tìm thấy ca làm hoặc đã check-out rồi."