from .db_connection import get_connection

class InventoryModel:
    def add_ingredient(self, name, unit, quantity, min_threshold):
        sql = """
            INSERT INTO ingredients (name, unit, stock_quantity, min_threshold) 
            VALUES (%s, %s, %s, %s) 
            ON CONFLICT (name) DO UPDATE SET stock_quantity = ingredients.stock_quantity + EXCLUDED.stock_quantity
            RETURNING ingredient_id
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (name, unit, quantity, min_threshold))
                ing_id = cur.fetchone()["ingredient_id"]
            conn.commit()
        return ing_id

    def get_all_ingredients(self):
        sql = "SELECT * FROM ingredients ORDER BY ingredient_id"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    def get_ingredient_by_name(self, name):
        sql = "SELECT * FROM ingredients WHERE name = %s"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (name,))
                return cur.fetchone()

    def create_import_receipt(self, staff_id, total_amount):
        sql = "INSERT INTO import_receipts (staff_id, total_amount) VALUES (%s, %s) RETURNING receipt_id"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (staff_id, total_amount))
                receipt_id = cur.fetchone()["receipt_id"]
            conn.commit()
        return receipt_id

    def add_import_detail(self, receipt_id, ingredient_id, quantity, unit_price):
        sql = "INSERT INTO import_receipt_details (receipt_id, ingredient_id, quantity, unit_price) VALUES (%s, %s, %s, %s)"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (receipt_id, ingredient_id, quantity, unit_price))
                # Cập nhật tồn kho
                cur.execute("UPDATE ingredients SET stock_quantity = stock_quantity + %s WHERE ingredient_id = %s", (quantity, ingredient_id))
            conn.commit()

    def add_recipe(self, product_id, size_id, ingredient_id, quantity_needed):
        sql = """
            INSERT INTO recipes (product_id, size_id, ingredient_id, quantity_needed)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (product_id, size_id, ingredient_id) 
            DO UPDATE SET quantity_needed = EXCLUDED.quantity_needed
            RETURNING recipe_id
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (product_id, size_id, ingredient_id, quantity_needed))
                rec_id = cur.fetchone()["recipe_id"]
            conn.commit()
        return rec_id