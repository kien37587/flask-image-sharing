# Hướng Dẫn Deploy Website Image Sharing

## 📋 Tổng Quan
Website này là một ứng dụng Flask để chia sẻ hình ảnh với tính năng đăng ký, đăng nhập và upload ảnh.

## 🚀 Cách Deploy lên Heroku (Khuyến nghị cho người mới)

### Bước 1: Chuẩn bị
1. **Cài đặt Heroku CLI**:
   - Tải về từ: https://devcenter.heroku.com/articles/heroku-cli
   - Hoặc dùng command: `npm install -g heroku`

2. **Đăng ký tài khoản Heroku**:
   - Truy cập: https://signup.heroku.com/
   - Tạo tài khoản miễn phí

### Bước 2: Chuẩn bị mã nguồn

#### 2.1 Tối ưu requirements.txt
File `requirements.txt` đã được chuẩn bị sẵn. Nếu muốn tối ưu, bạn có thể:
- Xóa các package không cần thiết (numpy, pandas, sklearn, matplotlib, etc. - vì app Flask không cần)
- Giữ lại chỉ các package cần thiết:
```
Flask==3.1.2
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
Pillow==12.0.0
Werkzeug==3.1.3
gunicorn==21.2.0
```

#### 2.2 Cấu hình ứng dụng
File `Procfile` và `runtime.txt` đã được chuẩn bị sẵn:
- **Procfile**: Chỉ định cách chạy ứng dụng
- **runtime.txt**: Chỉ định phiên bản Python

### Bước 3: Deploy lên Heroku

#### 3.1 Đăng nhập Heroku
```bash
heroku login
```

#### 3.2 Tạo ứng dụng mới trên Heroku
```bash
heroku create ten-ung-dung-cua-ban
```

#### 3.3 Khởi tạo Git (nếu chưa có)
```bash
git init
git add .
git commit -m "Initial commit"
```

#### 3.4 Thêm Heroku remote
```bash
heroku git:remote -a ten-ung-dung-cua-ban
```

#### 3.5 Deploy
```bash
git push heroku main
```

**Lưu ý**: Nếu dùng branch `master`:
```bash
git push heroku master
```

### Bước 4: Thiết lập biến môi trường
Trên Heroku Dashboard:
1. Vào Settings → Config Vars
2. Thêm biến:
   - `SECRET_KEY`: Một chuỗi ngẫu nhiên bất kỳ (để bảo mật session)

```bash
heroku config:set SECRET_KEY="your-secret-key-here"
```

### Bước 5: Khởi động lại ứng dụng
```bash
heroku restart
```

### Bước 6: Mở ứng dụng
```bash
heroku open
```

## 🌐 Cách Deploy lên các nền tảng khác

### 1. Railway.app
1. Đăng ký tại: https://railway.app/
2. Tạo project mới
3. Connect GitHub repository
4. Railway tự động detect Flask và deploy

### 2. Render.com
1. Đăng ký tại: https://render.com/
2. Tạo Web Service mới
3. Connect GitHub repository
4. Chọn Python environment
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app`

### 3. PythonAnywhere
1. Đăng ký tại: https://www.pythonanywhere.com/
2. Upload files qua files tab
3. Tạo web app và chọn Flask
4. Chỉnh sửa WSGI file để trỏ đến `app.py`
5. Reload web app

## ⚠️ Lưu ý quan trọng khi deploy

### Vấn đề về Database
- **SQLLite** (hiện tại) không phù hợp cho production
- Cần migrate sang **PostgreSQL** cho Heroku

**Giải pháp**:
1. Heroku tự động cung cấp PostgreSQL cho dyno đã cài đặt `psycopg2-binary` (đã có trong requirements.txt)
2. Code đã hỗ trợ `DATABASE_URL` từ environment variable

### Vấn đề về File Upload
- Files upload sẽ bị mất khi dyno restart (do ephemeral filesystem)
- **Giải pháp**: Dùng cloud storage (AWS S3, Cloudinary, etc.)

### Static Files
- File `whitenoise` đã có trong requirements.txt - tốt cho static files
- Nhưng cần cấu hình trong app.py:

```python
from whitenoise import WhiteNoise
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')
```

## 🔒 Bảo mật

1. **SECRET_KEY**: Phải là một chuỗi ngẫu nhiên mạnh
2. **DATABASE**: Không commit file database.db lên Git
3. **Environment Variables**: Không hard-code credentials

## 📊 Monitoring

Sau khi deploy:
```bash
# Xem logs
heroku logs --tail

# Xem trạng thái
heroku ps

# Xem config
heroku config
```

## 🐛 Troubleshooting

### Lỗi: "Module not found"
- Kiểm tra requirements.txt
- Chạy: `pip install -r requirements.txt` local trước

### Lỗi: "Application Error"
- Xem logs: `heroku logs --tail`
- Kiểm tra Procfile format

### Lỗi: "Database locked"
- Migrate sang PostgreSQL
- Kiểm tra DATABASE_URL

## 📝 Checklist trước khi deploy

- [x] Procfile đã có
- [x] runtime.txt đã có  
- [x] requirements.txt đầy đủ dependencies
- [x] Gunicorn đã thêm vào requirements.txt
- [ ] Đã thêm whitenoise config vào app.py
- [ ] Đã set SECRET_KEY
- [ ] Đã test app local
- [ ] Đã tối ưu requirements.txt (xóa packages không cần)

## 🎯 Bước tiếp theo (Optional)

1. **Thêm database migration**: Flask-Migrate
2. **Cloud storage cho images**: AWS S3 hoặc Cloudinary
3. **CDN**: Cloudflare
4. **Custom domain**: Thêm domain riêng
5. **HTTPS**: Heroku tự động cung cấp
6. **CI/CD**: GitHub Actions

## 📞 Cần giúp đỡ?

- Heroku Docs: https://devcenter.heroku.com/articles/getting-started-with-python
- Flask Deployment: https://flask.palletsprojects.com/en/2.3.x/deploying/

