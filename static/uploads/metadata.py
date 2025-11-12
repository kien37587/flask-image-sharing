from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'change-me'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
METADATA_FILE = os.path.join(UPLOAD_FOLDER, 'metadata.json')
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_metadata():
    if not os.path.exists(METADATA_FILE):
        return []
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save_metadata(data):
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # placeholder: templates expect this route
    if request.method == 'POST':
        # implement registration logic as needed
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # placeholder: templates expect this route
    if request.method == 'POST':
        # implement login logic as needed
        return redirect(url_for('gallery'))
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # avoid name collisions
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{timestamp}{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)

            # record metadata
            metadata = load_metadata()
            entry = {
                "filename": filename,
                "uploader": "Anonymous",   # replace with current user when auth present
                "uploaded_on": datetime.utcnow().isoformat() + 'Z'
            }
            metadata.append(entry)
            save_metadata(metadata)

            return redirect(url_for('view_image', filename=filename))
        else:
            flash('File type not allowed')
            return redirect(request.url)
    return render_template('upload.html')

@app.route('/gallery')
def gallery():
    metadata = load_metadata()
    images = [item['filename'] for item in metadata]
    return render_template('gallery.html', images=images, year=datetime.utcnow().year)

@app.route('/view/<filename>')
def view_image(filename):
    metadata = load_metadata()
    img = next((item for item in metadata if item['filename'] == filename), None)
    if not img:
        return "Image not found", 404
    return render_template('view_image.html', image=img)

# Serve uploaded files (used by gallery.html -> url_for('uploads', filename=...) )
@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Also provide endpoint 'uploaded_file' for view_image.html which uses that name
@app.route('/uploaded/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)