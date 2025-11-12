from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session, jsonify
from werkzeug.utils import secure_filename
import os, json
from datetime import datetime
import base64
import re

app = Flask(__name__)
app.secret_key = 'change-me-locally-123'  # đổi nếu cần

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
METADATA_FILE = os.path.join(UPLOAD_FOLDER, 'metadata.json')
USERS_FILE = os.path.join(BASE_DIR, 'users.json')
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- helper: users ---
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        return {}
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(data):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- helper: metadata ---
def load_metadata():
    if not os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []
    try:
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f) or []
    except Exception:
        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []

def save_metadata(data):
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_image_to_user(username, image_entry):
    """If username exists in users.json, append a minimal image record to users[username]['images']."""
    if not username:
        return
    users = load_users()
    if username not in users:
        return
    user = users.get(username) or {}
    imgs = user.get('images') or []
    # store a compact record
    imgs.append({
        'id': image_entry.get('id') or image_entry.get('filename'),
        'filename': image_entry.get('filename'),
        'imageName': image_entry.get('imageName') or image_entry.get('filename'),
        'uploadedAt': image_entry.get('uploadedAt') or image_entry.get('uploaded_on')
    })
    user['images'] = imgs
    users[username] = user
    try:
        save_users(users)
    except Exception:
        app.logger.exception('Failed to save user images')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# --- routes ---
@app.context_processor
def inject_user():
    return dict(current_user=session.get('username'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = (request.form.get('password') or '').strip()
        if not username or not password:
            flash('Vui lòng nhập username và password.')
            return redirect(url_for('register'))
        users = load_users()
        if username in users:
            flash('Username đã tồn tại.')
            return redirect(url_for('register'))
        users[username] = {'password': password}
        save_users(users)
        session['username'] = username
        flash('Đã đăng ký và đăng nhập.')
        return redirect(url_for('gallery'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = (request.form.get('password') or '').strip()
        users = load_users()
        if username in users and users[username].get('password') == password:
            session['username'] = username
            flash('Đăng nhập thành công.')
            return redirect(url_for('gallery'))
        flash('Sai username hoặc password.')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Đã đăng xuất.')
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Không tìm thấy file.')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Chưa chọn file.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename_raw = secure_filename(file.filename)
            ts = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            name, ext = os.path.splitext(filename_raw)
            filename = f"{name}_{ts}{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            # create an id for this upload so it can be referenced in users.json
            image_id = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            metadata = load_metadata()
            entry = {
                'id': image_id,
                "filename": filename,
                "uploader": session.get('username', 'Anonymous'),
                "uploaded_on": datetime.utcnow().isoformat() + 'Z'
            }
            metadata.append(entry)
            save_metadata(metadata)
            # also add a compact record to the uploader's user entry
            add_image_to_user(session.get('username'), entry)
            flash('Upload thành công.')
            return redirect(url_for('view_image', filename=filename))
        else:
            flash('Loại file không được phép.')
            return redirect(request.url)
    return render_template('upload.html')

@app.route('/gallery')
def gallery():
    metadata = load_metadata()
    images = metadata  # list of dicts: filename/uploader/uploaded_on
    return render_template('gallery.html', images=images, year=datetime.utcnow().year)

@app.route('/view/<filename>')
def view_image(filename):
    metadata = load_metadata()
    img = next((i for i in metadata if i.get('filename') == filename), None)
    if not img:
        return "Image not found", 404
    return render_template('view_image.html', image=img)


@app.route('/user')
def user_page():
    # render the user profile page (templates/user.html)
    username = session.get('username')
    users = load_users()
    profile = users.get(username, {}) if username else {}
    return render_template('user.html', profile=profile)


@app.route('/edit', methods=['GET', 'POST'])
def edit_profile():
    username = session.get('username')
    if not username:
        flash('Vui lòng đăng nhập trước khi chỉnh sửa hồ sơ.')
        return redirect(url_for('login'))
    users = load_users()
    user = users.get(username, {})
    if request.method == 'POST':
        full_name = (request.form.get('full_name') or '').strip()
        bio = (request.form.get('bio') or '').strip()
        user['full_name'] = full_name
        user['bio'] = bio
        users[username] = user
        save_users(users)
        flash('Đã cập nhật hồ sơ.')
        return redirect(url_for('user_page'))
    return render_template('edit.html', user=user)

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# serve the small SDK files expected by the templates
@app.route('/_sdk/<path:filename>')
def sdk_files(filename):
    sdk_dir = os.path.join(BASE_DIR, 'static', '_sdk')
    return send_from_directory(sdk_dir, filename)

# some templates may reference 'uploaded_file' endpoint
@app.route('/uploaded/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# simple API to list images (optional, used by JS)
@app.route('/api/images')
def api_images():
    # Return images with a public URL for imageData to be used directly in templates
    metadata = load_metadata()
    images = []
    for item in metadata:
        img = item.copy()
        # if filename exists, expose a URL
        if img.get('filename'):
            img['imageData'] = url_for('uploads', filename=img['filename'], _external=False)
        images.append(img)
    return jsonify(images)


@app.route('/api/images', methods=['POST'])
def api_create_image():
    """Expect JSON with fields: id, imageName, imageCategory, imageData (data URL)."""
    payload = request.get_json()
    if not payload:
        return jsonify({'isOk': False, 'error': 'Invalid JSON'}), 400
    image_data = payload.get('imageData')
    image_name = payload.get('imageName') or 'untitled'
    image_category = payload.get('imageCategory') or ''
    image_id = payload.get('id') or datetime.utcnow().strftime('%Y%m%d%H%M%S%f')

    # data URL -> save file
    m = None
    if isinstance(image_data, str):
        m = re.match(r'data:(image/[^;]+);base64,(.+)', image_data)
    if not m:
        return jsonify({'isOk': False, 'error': 'imageData must be a data URL'}), 400

    mime, b64 = m.group(1), m.group(2)
    ext = mimetype_to_ext(mime)
    filename = secure_filename(f"{image_id}{ext}")
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        with open(save_path, 'wb') as f:
            f.write(base64.b64decode(b64))
    except Exception as e:
        app.logger.exception('Failed to write image file')
        return jsonify({'isOk': False, 'error': str(e)}), 500

    try:
        metadata = load_metadata()
        entry = {
            'id': image_id,
            'imageName': image_name,
            'imageCategory': image_category,
            'filename': filename,
            'uploadedAt': payload.get('uploadedAt') or datetime.utcnow().isoformat() + 'Z',
            'uploader': session.get('username', 'Anonymous')
        }
        metadata.append(entry)
        save_metadata(metadata)
        # also add a compact record to the uploader's user entry
        try:
            add_image_to_user(session.get('username'), entry)
        except Exception:
            app.logger.exception('Failed to add image to user after API create')
        return jsonify({'isOk': True, 'data': entry})
    except Exception as e:
        app.logger.exception('Failed to save metadata')
        return jsonify({'isOk': False, 'error': str(e)}), 500


@app.route('/api/images/<image_id>', methods=['DELETE'])
def api_delete_image(image_id):
    metadata = load_metadata()
    idx = next((i for i, it in enumerate(metadata) if it.get('id') == image_id), None)
    if idx is None:
        return jsonify({'isOk': False, 'error': 'not found'}), 404
    entry = metadata.pop(idx)
    # remove file if exists
    if entry.get('filename'):
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, entry['filename']))
        except Exception:
            pass
    save_metadata(metadata)
    # remove from uploader's record if present
    uploader = entry.get('uploader')
    if uploader and uploader != 'Anonymous':
        try:
            users = load_users()
            if uploader in users:
                user = users.get(uploader) or {}
                imgs = user.get('images') or []
                imgs = [it for it in imgs if it.get('id') != image_id and it.get('filename') != entry.get('filename')]
                user['images'] = imgs
                users[uploader] = user
                save_users(users)
        except Exception:
            app.logger.exception('Failed to remove image reference from user')
    return jsonify({'isOk': True})


def mimetype_to_ext(mime):
    # minimal mapping
    mapping = {
        'image/png': '.png',
        'image/jpeg': '.jpg',
        'image/jpg': '.jpg',
        'image/gif': '.gif',
        'image/webp': '.webp'
    }
    return mapping.get(mime, '')


@app.route('/_diag')
def diag():
    # quick diagnostics to help debug environment and file permissions
    try:
        files = []
        for name in os.listdir(UPLOAD_FOLDER):
            files.append(name)
    except Exception as e:
        files = f'error listing uploads: {e}'

    return jsonify({
        'app_root': BASE_DIR,
        'upload_folder': UPLOAD_FOLDER,
        'upload_folder_exists': os.path.exists(UPLOAD_FOLDER),
        'upload_folder_writable': os.access(UPLOAD_FOLDER, os.W_OK),
        'metadata_file': METADATA_FILE,
        'metadata_exists': os.path.exists(METADATA_FILE),
        'metadata_preview': (load_metadata()[:10] if os.path.exists(METADATA_FILE) else []),
        'users_file': USERS_FILE,
        'users_exists': os.path.exists(USERS_FILE),
        'users_preview': load_users(),
        'uploads_list': files
    })

if __name__ == '__main__':
    app.run(debug=True)
