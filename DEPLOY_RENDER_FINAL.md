# 🚀 HƯỚNG DẪN DEPLOY RENDER - HOÀN CHỈNH

## ✅ Đã Fix Tất Cả Vấn Đề!

- ✅ Fix PostgreSQL URL (postgres:// → postgresql://)
- ✅ Code đã sẵn sàng deploy
- ✅ Git đã commit

---

## 📝 CÁC BƯỚC CUỐI CÙNG

### BƯỚC 1: Push lên GitHub

Bạn cần tạo GitHub repository trước (nếu chưa có):

1. Vào: **https://github.com/new**
2. Repository name: `flask-image-sharing`
3. **KHÔNG** tick bất kỳ checkbox nào
4. Click **Create repository**

**Sau đó chạy** (thay YOUR_USERNAME và flask-image-sharing):

```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/flask-image-sharing.git
git push -u origin main
```

---

### BƯỚC 2: Deploy lên Render

1. **Đăng ký**: https://render.com
   - **Get Started for Free**
   - **Sign up with GitHub**
   - Authorize Render

2. **Tạo Web Service**:
   - Dashboard → **New +** → **Web Service**
   - **Connect** repository
   - Chọn repo của bạn → **Connect**

3. **Cấu hình** (QUAN TRỌNG!):
   - **Name**: `flask-image-sharing` (hoặc tùy ý)
   - **Region**: **Singapore** (gần VN nhất)
   - **Branch**: `main`
   - **Root Directory**: `./` (để trống)
   - **Runtime**: **Python 3**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: **Free**
   - Click **Create Web Service**

4. **Set Environment Variables**:
   - Settings → **Environment** → **Add Environment Variable**
   - Key: `SECRET_KEY`
   - Value: random string dài (ví dụ: `my-super-secret-key-12345-dont-share`)
   - Click **Save Changes**

5. **Tạo PostgreSQL Database**:
   - Dashboard → **New +** → **PostgreSQL**
   - Name: `flask-db` (hoặc tùy ý)
   - **Free** tier
   - Region: **Singapore**
   - Click **Create Database**
   - Copy **Internal Database URL**
   - Vào Web Service → Settings → Environment
   - Add variable:
     - Key: `DATABASE_URL`
     - Value: Paste Internal Database URL
   - Save

---

### BƯỚC 3: Chờ Deploy

- Render tự động build và deploy
- Đợi 5-15 phút
- Click vào URL để xem website!

---

## ✅ XONG! Website Live!

URL của bạn: `https://flask-image-sharing.onrender.com`

---

## 🎓 GHI CHÚ QUAN TRỌNG

### Database:
- Render cung cấp PostgreSQL FREE
- Database URL tự động được inject vào environment
- Code đã fix để handle postgres:// URL

### Free Tier:
- Sleep sau 15 phút idle
- First request wake ~30s
- Data persistent

### Auto-deploy:
- Mỗi lần push lên GitHub → auto redeploy
- Không cần làm gì thêm!

---

## 🆘 TROUBLESHOOTING

### Build failed:
```bash
# Xem logs
Render → Logs tab
```

### Database error:
- Check DATABASE_URL đã set chưa
- Check PostgreSQL service đã tạo chưa

### 502 Bad Gateway:
- Đợi thêm 5 phút (build đang chạy)
- Check logs xem lỗi gì

---

## 📊 CHECKLIST CUỐI CÙNG

- [ ] Có GitHub repository
- [ ] Push code lên GitHub
- [ ] Sign up Render
- [ ] Tạo Web Service
- [ ] Set SECRET_KEY
- [ ] Tạo PostgreSQL Database
- [ ] Set DATABASE_URL
- [ ] Deploy thành công
- [ ] Test website

---

**Chúc mừng! Website của bạn đã live! 🎉**

