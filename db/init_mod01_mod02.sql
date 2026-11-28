CREATE TABLE IF NOT EXISTS roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS staff (
    staff_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL UNIQUE,
    dob DATE,
    address TEXT,
    email VARCHAR(100) UNIQUE,
    hire_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(30) NOT NULL DEFAULT 'Đang làm việc'
);

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    staff_id INT NOT NULL UNIQUE REFERENCES staff(staff_id),
    role_id INT NOT NULL REFERENCES roles(role_id),
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    failed_attempts INT NOT NULL DEFAULT 0 CHECK (failed_attempts >= 0),
    locked_until TIMESTAMP NULL,
    last_login TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    category_id INT NOT NULL REFERENCES categories(category_id),
    product_name VARCHAR(150) NOT NULL UNIQUE,
    base_price DECIMAL(10, 2) NOT NULL CHECK (base_price >= 0),
    description TEXT,
    image_url VARCHAR(255),
    status VARCHAR(30) NOT NULL DEFAULT 'Còn hàng'
);

CREATE TABLE IF NOT EXISTS sizes (
    size_id SERIAL PRIMARY KEY,
    size_name VARCHAR(10) NOT NULL UNIQUE,
    extra_price DECIMAL(10, 2) NOT NULL DEFAULT 0 CHECK (extra_price >= 0)
);

CREATE TABLE IF NOT EXISTS toppings (
    topping_id SERIAL PRIMARY KEY,
    topping_name VARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    status VARCHAR(30) NOT NULL DEFAULT 'Còn hàng'
);

INSERT INTO roles (role_name, description) VALUES
    ('Owner', 'Chủ cửa hàng'),
    ('Manager', 'Quản lý cửa hàng'),
    ('Cashier', 'Nhân viên thu ngân'),
    ('Order', 'Nhân viên order'),
    ('Barista', 'Nhân viên pha chế')
ON CONFLICT (role_name) DO NOTHING;

INSERT INTO staff (full_name, phone, email, status) VALUES
    ('Nguyễn Thanh Trúc', '0905111222', 'truc.mod0102@noname.vn', 'Đang làm việc')
ON CONFLICT (phone) DO NOTHING;