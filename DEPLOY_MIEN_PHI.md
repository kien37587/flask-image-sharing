# 🆓 Deploy Miễn Phí - Không Cần Thẻ Tín Dụng

## ✅ 3 Platform Miễn Phí Hoàn Toàn:

### 1. 🏆 Render.com (KHUYẾN NGHỊ - Tốt nhất)
- ✅ 100% miễn phí
- ✅ Không cần thẻ
- ✅ 750 giờ/tháng free
- ✅ Auto-deploy từ GitHub
- ⚠️ Auto-sleep sau 15 phút không dùng (wake lên khi có người truy cập)

### 2. 🐍 PythonAnywhere
- ✅ 100% miễn phí
- ✅ Không cần thẻ
- ✅ Free forever
- ❌ Cần upload files thủ công
- ❌ Hạn chế hơn

### 3. 🚀 Fly.io
- ✅ Miễn phí
- ✅ Không cần thẻ
- ✅ Global CDN
- ⚠️ Hơi phức tạp setup

---

## 🎯 OPTION 1: Render.com (KHUYẾN NGHỊ)

### Bước 1: Tạo GitHub Repository

Nếu bạn chưa có GitHub repo:

```powershell
# Tạo repo trên GitHub.com
# Vào: https://github.com/new

# Sau đó chạy (thay YOUR_USERNAME và REPO_NAME):
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/flask-image-sharing.git
git push -u origin main
```

### Bước 2: Deploy lên Render

1. **Đăng ký**: https://render.com
   - Click **Sign Up** → **Sign up with GitHub**
   - Authorize Render

2. **Tạo Web Service**:
   - Dashboard → **New +** → **Web Service**
   - **Connect** repository của bạn
   - Chọn repo → **Connect**

3. **Cấu hình**:
   - **Name**: `flask-image-sharing` (tùy chọn)
   - **Region**: Singapore (gần VN nhất)
   - **Branch**: `main`
   - **Root Directory**: `./` (để trống)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: **Free**
   - Click **Create Web Service**

4. **Set Environment Variable**:
   - Settings → Environment → Add Environment Variable
   - Key: `SECRET_KEY`
   - Value: random string (ví dụ: `my-secret-key-12345`)
   - Click **Save Changes**

5. **Deploy**:
   - Render tự động deploy
   - Đợi ~5-10 phút
   - Click vào link để xem website

### ⚠️ Lưu ý Render:
- Website sleep sau 15 phút không dùng
- Lần đầu wake mất ~30 giây
- Database sẽ reset khi redeploy

---

## 🎯 OPTION 2: PythonAnywhere

### Bước 1: Upload Files

1. **Đăng ký**: https://www.pythonanywhere.com
2. **Free Account** → Login
3. Vào **Files** tab
4. **Upload a file** → Chọn tất cả files trong project
   - app.py
   - requirements.txt
   - Procfile
   - runtime.txt
   - templates/
   - static/

### Bước 2: Tạo Web App

1. Vào **Web** tab
2. Click **Add a new web app**
3. Chọn **Flask** → **Python 3.9**
4. Nhập đường dẫn: `/home/yourusername/flask-image-sharing/app.py`

### Bước 3: Cấu hình

1. Web tab → **Static files mapping**
2. Add mapping:
   - URL: `/static/`
   - Directory: `/home/yourusername/mysite/static/`

3. **Files** → `wsgi.py`
4. Sửa thành:

```python
import sys

# add your project directory to sys.path
project_home = '/home/yourusername'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# import Flask app (but we need to call it "application" for WSGI)
from app import app as application
```

5. **Reload** web app
6. Xong!

---

## 🎯 OPTION 3: Fly.io (Advanced)

### Bước 1: Cài Fly CLI

```powershell
# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### Bước 2: Login

```powershell
fly auth login
```

### Bước 3: Init

```powershell
fly launch
```

### Bước 4: Deploy

```powershell
fly deploy
```

---

## 📊 SO SÁNH

| Platform | Miễn phí | Dễ setup | Auto-deploy | Sleep? | Tốc độ |
|----------|----------|----------|-------------|--------|--------|
| **Render** | ✅ | ⭐⭐⭐⭐⭐ | ✅ | ⚠️ 15 phút | ⚡⚡⚡ |
| **PythonAnywhere** | ✅ | ⭐⭐⭐ | ❌ | ❌ | ⚡⚡ |
| **Fly.io** | ✅ | ⭐⭐ | ✅ | ❌ | ⚡⚡⚡⚡ |

---

## 🏆 KHUYẾN NGHỊ

→ **Dùng Render.com** vì:
1. ✅ Setup đơn giản nhất
2. ✅ Auto-deploy từ GitHub
3. ✅ UI đẹp, dễ quản lý
4. ✅ Free tier tốt
5. ✅ Không cần thẻ

---

## 🎓 HƯỚNG DẪN CHI TIẾT RENDER

Chi tiết từng bước deploy Render:

### 1. GitHub Setup
- Tạo repo GitHub
- Push code lên

### 2. Render Setup
- Sign up với GitHub
- New Web Service
- Connect repo
- Config build/start commands
- Set SECRET_KEY

### 3. Deploy
- Render tự động build
- Chờ 5-10 phút
- Xem log: Render UI → Logs tab

---

## 🆘 TROUBLESHOOTING

### Render:
- **Build failed**: Check `requirements.txt`
- **502 Error**: Check `gunicorn` trong requirements
- **Sleep too slow**: Nâng cấp paid tier

### PythonAnywhere:
- **Import error**: Check sys.path trong wsgi.py
- **404 on static**: Check static files mapping

---

## 📝 CHECKLIST

- [ ] Tạo GitHub repo
- [ ] Push code lên GitHub
- [ ] Chọn platform (Render/PythonAnywhere)
- [ ] Deploy
- [ ] Set SECRET_KEY
- [ ] Test website
- [ ] Celebrate! 🎉

---

**Good luck! 🚀**

