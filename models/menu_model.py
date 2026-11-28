from .db_connection import get_connection


class MenuModel:
    def create_category(self, category_name: str, description: str = "", is_active: bool = True) -> int:
        sql = """
            INSERT INTO categories (category_name, description, is_active)
            VALUES (%s, %s, %s)
            RETURNING category_id
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (category_name, description, is_active))
                cat_id = cur.fetchone()["category_id"]
            conn.commit()
        return cat_id

    def set_category_active(self, category_id: int, is_active: bool):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE categories SET is_active = %s WHERE category_id = %s", (is_active, category_id))
                if not is_active:
                    cur.execute(
                        "UPDATE products SET status = 'Hết hàng' WHERE category_id = %s",
                        (category_id,),
                    )
            conn.commit()

    def create_product(self, category_id: int, product_name: str, base_price: float, description: str = "", image_url: str = "") -> int:
        sql = """
            INSERT INTO products (category_id, product_name, base_price, description, image_url, status)
            VALUES (%s, %s, %s, %s, %s, 'Còn hàng')
            RETURNING product_id
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (category_id, product_name, base_price, description, image_url))
                prod_id = cur.fetchone()["product_id"]
            conn.commit()
        return prod_id

    def update_product_price(self, product_id: int, base_price: float):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE products SET base_price = %s WHERE product_id = %s", (base_price, product_id))
            conn.commit()

    def update_product_status(self, product_id: int, status: str):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE products SET status = %s WHERE product_id = %s", (status, product_id))
            conn.commit()

    def upsert_size(self, size_name: str, extra_price: float) -> int:
        sql = """
            INSERT INTO sizes (size_name, extra_price)
            VALUES (%s, %s)
            ON CONFLICT (size_name)
            DO UPDATE SET extra_price = EXCLUDED.extra_price
            RETURNING size_id
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (size_name, extra_price))
                size_id = cur.fetchone()["size_id"]
            conn.commit()
        return size_id

    def create_topping(self, topping_name: str, price: float, status: str = "Còn hàng") -> int:
        sql = """
            INSERT INTO toppings (topping_name, price, status)
            VALUES (%s, %s, %s)
            RETURNING topping_id
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (topping_name, price, status))
                top_id = cur.fetchone()["topping_id"]
            conn.commit()
        return top_id

    def set_topping_status(self, topping_id: int, status: str):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE toppings SET status = %s WHERE topping_id = %s", (status, topping_id))
            conn.commit()

    def topping_has_order_history(self, topping_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT to_regclass('public.order_detail_toppings') AS tbl")
                tbl = cur.fetchone()["tbl"]
                if not tbl:
                    return False
                cur.execute("SELECT 1 FROM order_detail_toppings WHERE topping_id = %s LIMIT 1", (topping_id,))
                return cur.fetchone() is not None