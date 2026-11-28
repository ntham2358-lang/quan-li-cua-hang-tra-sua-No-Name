from controllers.auth_controller import AuthController
from controllers.menu_controller import MenuController
from models.auth_user_model import AuthUserModel
from models.menu_model import MenuModel
from views.console_view import ConsoleView


def main():
    view = ConsoleView()
    auth_model = AuthUserModel()
    menu_model = MenuModel()

    auth_ctrl = AuthController(auth_model)
    menu_ctrl = MenuController(menu_model)

    # 1. Tạo tài khoản mẫu cho nhân viên (staff_id=1 vừa tạo ở Bước 1) nếu chưa có
    if not auth_model.get_user_by_username("truc_owner"):
        ok, msg = auth_ctrl.create_staff_account(
            actor_role="Owner",
            staff_id=1,
            role_name="Owner",
            username="truc_owner",
            raw_password="Password123",
        )
        view.show(ok, msg)

    # 2. Đăng nhập kiểm tra MOD-01
    ok, res = auth_ctrl.login("truc_owner", "Password123")
    view.show(ok, res)
    if not ok:
        return

    actor_role = res["role"]

    # 3. Chạy thử MOD-02: Danh mục, Size, Topping, Món
    ok, msg = menu_ctrl.add_category(actor_role, "Trà sữa", "Nhóm trà sữa quán No Name")
    view.show(ok, msg)

    view.show(*menu_ctrl.set_size(actor_role, "M", 0))
    view.show(*menu_ctrl.set_size(actor_role, "L", 8000))
    view.show(*menu_ctrl.add_topping(actor_role, "Trân châu đen", 6000))
    view.show(*menu_ctrl.add_product(actor_role, 1, "Trà sữa truyền thống", 25000, "Đậm vị trà"))


if __name__ == "__main__":
    main()