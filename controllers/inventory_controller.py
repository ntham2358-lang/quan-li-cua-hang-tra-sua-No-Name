class InventoryController:
    def __init__(self, model):
        self.model = model

    def add_ingredient(self, actor_role, name, unit, quantity, min_threshold):
        if actor_role not in ("Owner", "Manager"):
            return False, "Không có quyền quản lý kho."
        if quantity < 0 or min_threshold < 0:
            return False, "Số lượng không được âm."
        
        ing_id = self.model.add_ingredient(name.strip(), unit.strip(), quantity, min_threshold)
        return True, f"Đã thêm nguyên liệu '{name}' (ID: {ing_id})."

    def create_import(self, actor_role, staff_id, items):
        # items là list các dict: [{'name': 'Trà đen', 'quantity': 1000, 'price': 50000}]
        if actor_role not in ("Owner", "Manager"):
            return False, "Không có quyền nhập kho."
        
        total_amount = sum(item['quantity'] * item['price'] for item in items)
        receipt_id = self.model.create_import_receipt(staff_id, total_amount)

        for item in items:
            ing = self.model.get_ingredient_by_name(item['name'])
            if not ing:
                return False, f"Không tìm thấy nguyên liệu {item['name']}."
            self.model.add_import_detail(receipt_id, ing['ingredient_id'], item['quantity'], item['price'])
        
        return True, f"Đã tạo phiếu nhập kho #{receipt_id}. Tổng tiền: {total_amount} VNĐ."

    def setup_recipe(self, actor_role, product_id, size_id, ingredient_name, quantity_needed):
        if actor_role not in ("Owner", "Manager"):
            return False, "Không có quyền thiết lập định lượng."
        
        ing = self.model.get_ingredient_by_name(ingredient_name)
        if not ing:
            return False, "Không tìm thấy nguyên liệu."
        
        self.model.add_recipe(product_id, size_id, ing['ingredient_id'], quantity_needed)
        return True, f"Đã thêm định lượng cho món ID {product_id}."