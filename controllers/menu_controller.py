class MenuController:
    def __init__(self, model):
        self.model = model

    def add_category(self, actor_role: str, name: str, description: str = ""):
        if actor_role not in ("Owner", "Manager"):
            return False, "Không có quyền quản lý danh mục."
        if not name.strip():
            return False, "Tên danh mục không được để trống."
        cat_id = self.model.create_category(name.strip(), description.strip(), True)
        return True, f"Đã thêm danh mục (category_id={cat_id})."

    def toggle_category(self, actor_role: str, category_id: int, is_active: bool):
        if actor_role not in ("Owner", "Manager"):
            return False, "Không có quyền cập nhật danh mục."
        self.model.set_category_active(category_id, is_active)
        return True, "Đã cập nhật trạng thái danh mục (và ẩn món liên kết nếu tắt danh mục)."

    def add_product(self, actor_role: str, category_id: int, name: str, base_price: float, description: str = "", image_url: str = ""):
        if actor_role not in ("Owner", "Manager"):
            return False, "Không có quyền thêm món."
        if not name.strip() or base_price < 0:
            return False, "Tên món không hợp lệ hoặc giá bán < 0."
        prod_id = self.model.create_product(category_id, name.strip(), base_price, description.strip(), image_url.strip())
        return True, f"Đã thêm món (product_id={prod_id})."

    def change_product_price(self, actor_role: str, product_id: int, new_price: float):
        if actor_role not in ("Owner", "Manager"):
            return False, "Không có quyền đổi giá."
        if new_price < 0:
            return False, "Giá bán phải >= 0."
        self.model.update_product_price(product_id, new_price)
        return True, "Đã cập nhật giá bán (không áp dụng hồi tố đơn cũ/đang chờ thanh toán)."

    def change_product_status(self, actor_role: str, product_id: int, status: str):
        if actor_role not in ("Owner", "Manager"):
            return False, "Không có quyền đổi trạng thái món."
        if status not in ("Còn hàng", "Hết hàng"):
            return False, "Trạng thái món phải là 'Còn hàng' hoặc 'Hết hàng'."
        self.model.update_product_status(product_id, status)
        return True, f"Đã đổi trạng thái món -> {status}."

    def set_size(self, actor_role: str, size_name: str, extra_price: float):
        if actor_role not in ("Owner", "Manager"):
            return False, "Không có quyền thiết lập size."
        if not size_name.strip() or extra_price < 0:
            return False, "Tên size hoặc giá phụ thu không hợp lệ."
        size_id = self.model.upsert_size(size_name.strip().upper(), extra_price)
        return True, f"Đã lưu size (size_id={size_id})."

    def add_topping(self, actor_role: str, name: str, price: float):
        if actor_role not in ("Owner", "Manager"):
            return False, "Không có quyền thêm topping."
        if not name.strip() or price < 0:
            return False, "Tên topping hoặc giá không hợp lệ."
        top_id = self.model.create_topping(name.strip(), price, "Còn hàng")
        return True, f"Đã thêm topping (topping_id={top_id})."

    def retire_topping(self, actor_role: str, topping_id: int):
        if actor_role not in ("Owner", "Manager"):
            return False, "Không có quyền cập nhật topping."
        self.model.set_topping_status(topping_id, "Ngừng bán")
        if self.model.topping_has_order_history(topping_id):
            return True, "Topping đã có lịch sử đơn hàng -> chuyển sang 'Ngừng bán' thay vì xóa cứng."
        return True, "Đã chuyển topping sang trạng thái 'Ngừng bán'."