-- MOD-05: Kho và Định lượng
CREATE TABLE IF NOT EXISTS ingredients (
    ingredient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    unit VARCHAR(20) NOT NULL,
    stock_quantity DECIMAL(10, 2) NOT NULL DEFAULT 0,
    min_threshold DECIMAL(10, 2) NOT NULL DEFAULT 10,
    status VARCHAR(30) NOT NULL DEFAULT 'Còn hàng'
);

CREATE TABLE IF NOT EXISTS recipes (
    recipe_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(product_id),
    size_id INT REFERENCES sizes(size_id),
    ingredient_id INT NOT NULL REFERENCES ingredients(ingredient_id),
    quantity_needed DECIMAL(10, 2) NOT NULL CHECK (quantity_needed > 0),
    UNIQUE(product_id, size_id, ingredient_id)
);

CREATE TABLE IF NOT EXISTS import_receipts (
    receipt_id SERIAL PRIMARY KEY,
    staff_id INT NOT NULL REFERENCES staff(staff_id),
    total_amount DECIMAL(12, 2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) NOT NULL DEFAULT 'Hoàn thành'
);

CREATE TABLE IF NOT EXISTS import_receipt_details (
    detail_id SERIAL PRIMARY KEY,
    receipt_id INT NOT NULL REFERENCES import_receipts(receipt_id),
    ingredient_id INT NOT NULL REFERENCES ingredients(ingredient_id),
    quantity DECIMAL(10, 2) NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0)
);

-- MOD-06: Ca làm và Chấm công
CREATE TABLE IF NOT EXISTS shifts (
    shift_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS shift_assignments (
    assignment_id SERIAL PRIMARY KEY,
    staff_id INT NOT NULL REFERENCES staff(staff_id),
    shift_id INT NOT NULL REFERENCES shifts(shift_id),
    work_date DATE NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Đã phân công',
    UNIQUE(staff_id, shift_id, work_date)
);

CREATE TABLE IF NOT EXISTS attendance (
    attendance_id SERIAL PRIMARY KEY,
    staff_id INT NOT NULL REFERENCES staff(staff_id),
    shift_id INT NOT NULL REFERENCES shifts(shift_id),
    work_date DATE NOT NULL,
    check_in TIMESTAMP,
    check_out TIMESTAMP,
    note TEXT,
    UNIQUE(staff_id, shift_id, work_date)
);

-- Thêm sẵn vài Ca làm việc mẫu
INSERT INTO shifts (name, start_time, end_time) VALUES
    ('Ca Sáng', '08:00', '12:00'),
    ('Ca Chiều', '12:00', '17:00'),
    ('Ca Tối', '17:00', '23:00')
ON CONFLICT (name) DO NOTHING;

-- Thêm sẵn vài nguyên liệu mẫu
INSERT INTO ingredients (name, unit, stock_quantity, min_threshold) VALUES
    ('Trà đen', 'g', 5000, 1000),
    ('Sữa đặc', 'ml', 2000, 500),
    ('Trân châu', 'g', 3000, 500)
ON CONFLICT (name) DO NOTHING;