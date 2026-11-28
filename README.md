# Hướng dẫn kết nối Django với PostgreSQL trên Supabase

## 1. Thông tin Database

Dự án sử dụng PostgreSQL được lưu trữ trên Supabase.

| Thông tin | Giá trị |
|---|---|
| Database Host | `db.gatffuwdsfknaqgpgcnk.supabase.co` |
| Port | `5432` |
| Database Name | `postgres` |
| Username | `postgres` |
| SSL Mode | `require` |
| Database | PostgreSQL |
| Backend | Django (Python) |

**Lưu ý:** Không đưa mật khẩu database vào README hoặc GitHub.

## 2. Cài đặt thư viện cần thiết

Mở Terminal tại thư mục dự án, kích hoạt môi trường ảo:

```powershell
.venv\Scripts\Activate
```

Cài đặt các thư viện:

```powershell
pip install django
pip install "psycopg[binary]"
pip install python-dotenv
```

## 3. Tạo file .env

Tạo file `.env` tại thư mục gốc dự án, cùng cấp với `manage.py`.

Nội dung:

```env
DB_HOST=db.gatffuwdsfknaqgpgcnk.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=YOUR_DATABASE_PASSWORD
DB_SSLMODE=require
```

Thay `YOUR_DATABASE_PASSWORD` bằng mật khẩu database mới của bạn.

**Không commit file `.env` lên GitHub.**

## 4. Cấu hình Django

Mở file `config/settings.py`.


Tìm biến `DATABASES` và kiểm tra xem cấu hình đã giống như này chx 

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': os.getenv('DB_SSLMODE', 'require'),
        },
    }
}
```

## 5. Kiểm tra kết nối Database

Chạy lệnh:

```powershell
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('KET NOI DATABASE THANH CONG!')"
```

Nếu kết nối thành công, Terminal sẽ hiển thị:

```text
KET NOI DATABASE THANH CONG!
```

## 6. Tạo các bảng hệ thống Django

Sau khi kết nối thành công, chạy:

```powershell
python manage.py migrate
```

Nếu các migration chạy thành công và xuất hiện trạng thái `OK`, Django đã tạo các bảng hệ thống trên Supabase.

## 7. Cấu hình .gitignore(bắt buộc)

Mở hoặc tạo file `.gitignore` ở thư mục gốc dự án.

Thêm nội dung:

```gitignore
# Environment
.env
.venv/

# Python
__pycache__/
*.py[cod]

# Django
staticfiles/
media/
```

## 8. Hướng dẫn cho thành viên trong nhóm

Khi tải source code từ GitHub:

1. Clone repository về máy.
2. Tạo môi trường ảo `.venv`.
3. Cài đặt các thư viện cần thiết.
4. Tạo file `.env` riêng trên máy.
5. Điền thông tin kết nối database được nhóm cung cấp qua kênh riêng tư.
6. Chạy `python manage.py migrate`.
7. Chạy `python manage.py runserver` để khởi động website.

**Lưu ý khi làm việc nhóm:**

- Source code được quản lý trên GitHub.
- Database được lưu trữ tập trung trên Supabase.
- Các thành viên kết nối tới cùng một database bằng thông tin được cấp riêng tư.
- Không đưa mật khẩu database lên GitHub.
- Các thay đổi cấu trúc database cần được quản lý bằng Django migrations.
- Nên thống nhất người tạo và quản lý migration để tránh xung đột.

## 9. Khởi chạy dự án

```powershell
python manage.py runserver
```

Truy cập website:

http://127.0.0.1:8000/
