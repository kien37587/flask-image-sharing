# 📘 Hướng Dẫn Tạo GitHub Repository và Deploy

## 🎯 Bước 1: Tạo Repository trên GitHub

### Cách làm:
1. Truy cập: **https://github.com/new**
2. Đăng nhập GitHub (hoặc đăng ký nếu chưa có)
3. Điền thông tin:
   - **Repository name**: `flask-image-sharing` (hoặc tên bạn muốn)
   - **Description**: "Flask Image Sharing App"
   - **Public** hoặc **Private** (tùy chọn)
   - **KHÔNG** tick "Add README"
   - **KHÔNG** tick "Add .gitignore" (đã có rồi)
   - **KHÔNG** tick "Choose a license"
4. Click **Create repository**

---

## 🎯 Bước 2: Connect Repository với Local Code

### Sau khi tạo repo, bạn sẽ thấy hướng dẫn. Copy URL repository của bạn:

Ví dụ: `https://github.com/YOUR_USERNAME/flask-image-sharing.git`

### Sau đó chạy các lệnh sau trong PowerShell:

```powershell
# Vào thư mục project
cd "C:\Users\pv\OneDrive\Máy tính\LTM"

# Xóa remote cũ
git remote remove origin

# Thêm remote mới (THAY URL CỦA BẠN)
git remote add origin https://github.com/YOUR_USERNAME/flask-image-sharing.git

# Push code lên
git push -u origin main
```

---

## 🎯 Bước 3: Deploy lên Railway

### Sau khi code đã lên GitHub:

1. Truy cập: **https://railway.app**
2. Login bằng GitHub
3. **New Project**
4. **Deploy from GitHub repo**
5. Chọn repository của bạn
6. Railway **tự động detect Flask**!
7. Click vào service → Settings → Generate domain

### XONG! Website đã live! 🎉

---

## 🔗 Quick Links

- Tạo repo: https://github.com/new
- Railway: https://railway.app
- GitHub của tôi: https://github.com (sau khi tạo repo)

---

## ⚡ Alternative: Deploy Render.com

Nếu không thích Railway, có thể dùng Render:

1. Tạo GitHub repo (như trên)
2. Vào: **https://render.com**
3. New → **Web Service**
4. Connect GitHub → Chọn repo
5. Cấu hình:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Deploy!

---

## 🎓 Tips

- Repository name có thể là bất kỳ gì
- Public repo: ai cũng thấy code
- Private repo: chỉ bạn thấy
- Railway/Render tự động detect Flask từ Procfile

---

**Good luck! 🚀**

