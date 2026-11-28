from controllers.inventory_controller import InventoryController
from controllers.shift_controller import ShiftController
from models.inventory_model import InventoryModel
from models.shift_model import ShiftModel
from views.console_view import ConsoleView
from models.db_connection import get_connection

def setup_mock_data():
    """Hàm này tự động thêm Category, Product và Size mẫu để test cho dễ"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            # 1. Thêm Danh mục
            cur.execute("INSERT INTO categories (category_name) VALUES ('Trà sữa test') ON CONFLICT DO NOTHING")
            cur.execute("SELECT category_id FROM categories LIMIT 1")
            cat_id = cur.fetchone()["category_id"]
            
            # 2. Thêm Món (ID sẽ là 1 nếu bảng trống)
            cur.execute("""
                INSERT INTO products (product_id, category_id, product_name, base_price) 
                VALUES (1, %s, 'Trà sữa mẫu', 25000) 
                ON CONFLICT (product_id) DO NOTHING
            """, (cat_id,))
            
            # 3. Thêm Size M (ID = 1)
            cur.execute("INSERT INTO sizes (size_id, size_name) VALUES (1, 'M') ON CONFLICT (size_id) DO NOTHING")
        conn.commit()

def main():
    view = ConsoleView()
    
    # Gọi hàm tạo dữ liệu mẫu trước khi test
    setup_mock_data()
    
    inv_model = InventoryModel()
    inv_ctrl = InventoryController(inv_model)
    
    shift_model = ShiftModel()
    shift_ctrl = ShiftController(shift_model)

    # Giả lập đăng nhập với quyền Quản lý (Manager) và staff_id = 1
    actor_role = "Manager"
    staff_id = 1

    print("\n--- TEST MOD-05: KHO & ĐỊNH LƯỢNG ---")
    # 1. Thêm nguyên liệu mới
    view.show(*inv_ctrl.add_ingredient(actor_role, "Đường phèn", "g", 10000, 2000))
    
    # 2. Tạo phiếu nhập kho
    nhap_kho_items = [
        {"name": "Trà đen", "quantity": 500, "price": 100}, 
        {"name": "Trân châu", "quantity": 1000, "price": 50} 
    ]
    view.show(*inv_ctrl.create_import(actor_role, staff_id, nhap_kho_items))

    # 3. Cài đặt định lượng (Món số 1, Size M (id=1), cần 10g trà đen)
    view.show(*inv_ctrl.setup_recipe(actor_role, product_id=1, size_id=1, ingredient_name="Trà đen", quantity_needed=10))

    print("\n--- TEST MOD-06: CA LÀM & CHẤM CÔNG ---")
    # 1. Phân ca làm việc (Ca 1 là Ca Sáng) cho ngày hôm nay
    today = "2023-11-20" 
    view.show(*shift_ctrl.assign_shift(actor_role, staff_id, shift_id=1, work_date=today))

    # 2. Nhân viên Check-in
    view.show(*shift_ctrl.check_in(staff_id, shift_id=1, work_date=today))

    # 3. Nhân viên Check-out
    view.show(*shift_ctrl.check_out(staff_id, shift_id=1, work_date=today))

    print("\n--- KIỂM TRA LẠI DATABASE ---")
    ings = inv_model.get_all_ingredients()
    for i in ings:
        print(f"Nguyên liệu: {i['name']} | Tồn kho: {i['stock_quantity']} {i['unit']}")

if __name__ == "__main__":
    main()