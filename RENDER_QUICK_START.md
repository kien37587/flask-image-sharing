# ⚡ Deploy Render.com - 5 Bước (MIỄN PHÍ)

## 🎯 Render.com:
- ✅ 100% miễn phí
- ✅ Không cần thẻ
- ✅ Auto-deploy từ GitHub
- ⚠️ Sleep sau 15 phút không dùng (OK cho test)

---

## 📝 5 BƯỚC:

### BƯỚC 1: Có GitHub Repository
Bạn đã có rồi! Nếu chưa:

```powershell
# Vào https://github.com/new để tạo repo
# Sau đó:
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/flask-image-sharing.git
git push -u origin main
```

### BƯỚC 2: Đăng ký Render
1. Vào: **https://render.com**
2. Click **Get Started for Free**
3. **Sign up with GitHub**
4. Authorize Render

### BƯỚC 3: Tạo Web Service
1. Dashboard → **New +** → **Web Service**
2. Click **Connect** repository
3. Chọn repo của bạn → **Connect**

### BƯỚC 4: Cấu hình
Điền các thông tin:
- **Name**: `flask-app` (hoặc tùy ý)
- **Region**: **Singapore** (gần VN)
- **Branch**: `main`
- **Root Directory**: `./` (để trống)
- **Runtime**: **Python 3**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Instance Type**: **Free**

Click **Create Web Service**

### BƯỚC 5: Set Environment Variable
1. Click vào service vừa tạo
2. Vào **Environment** tab
3. **Add Environment Variable**:
   - Key: `SECRET_KEY`
   - Value: `your-super-secret-key-change-this-12345`
4. Click **Save Changes**

### CHỜ DEPLOY
- Render tự động build
- Đợi 5-10 phút
- Click vào URL để xem website!

---

## ✅ XONG! Website đã live!

URL của bạn: `https://flask-app.onrender.com` (hoặc tùy tên bạn đặt)

---

## 🎯 SETUP THÊM (Optional):

### Custom Domain:
Settings → Add Custom Domain

### Monitor:
Dashboard → Xem logs, metrics

### Auto-deploy:
Mỗi lần push code lên GitHub, Render tự động redeploy!

---

## 🆘 TROUBLESHOOTING:

### Build failed:
- Check `requirements.txt`
- Xem logs: Logs tab

### 502 Bad Gateway:
- Check `gunicorn` có trong requirements
- Check `Procfile` đúng chưa

### Timeout:
- Free tier slow hơn
- Đợi thêm 5 phút

---

## 📊 LƯU Ý:

### Free Tier:
- Sleep sau 15 phút idle
- First request wake ~30s
- Database ephemeral (mất data khi redeploy)

### Paid Tier ($7/tháng):
- Never sleep
- Faster
- Persistent database

---

**Good luck! 🚀**

