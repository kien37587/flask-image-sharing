# 🚀 Deploy Nhanh lên Heroku

## ⚡ 3 Bước Deploy

### Bước 1: Cài đặt Heroku CLI & Đăng nhập
```bash
# Cài Heroku CLI từ https://devcenter.heroku.com/articles/heroku-cli

# Đăng nhập
heroku login
```

### Bước 2: Tạo App và Push Code
```bash
# Di chuyển vào thư mục project
cd "C:\Users\pv\OneDrive\Máy tính\LTM"

# Khởi tạo Git (nếu chưa có)
git init
git add .
git commit -m "Initial deployment"

# Tạo app Heroku (đặt tên app của bạn)
heroku create your-app-name

# Deploy
git push heroku master
```

### Bước 3: Set Environment Variables
```bash
# Set SECRET_KEY (quan trọng!)
heroku config:set SECRET_KEY="your-random-secret-key-change-this"

# Mở website
heroku open
```

## ✅ Xong! Website đã live!

## 📝 Lưu ý:
- **Database**: Hiện đang dùng SQLite, Heroku sẽ tự migrate sang PostgreSQL
- **Upload**: Files sẽ mất khi restart dyno (cần dùng S3 sau này)
- **Logs**: Xem bằng `heroku logs --tail`

## 🔗 Link hữu ích:
- [Heroku Dashboard](https://dashboard.heroku.com)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)

## 🆘 Gặp vấn đề?
```bash
# Xem logs để debug
heroku logs --tail

# Restart app
heroku restart

# Xem config
heroku config
```

