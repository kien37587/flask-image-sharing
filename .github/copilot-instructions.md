# Guidance for AI coding agents working on this repository

This repository is a small Flask-based image-sharing web app. The goal for an AI agent is to make the codebase productive locally: run the app, ensure templates render, and maintain the simple upload/gallery flows.

High-level architecture

- app.py: single Flask process that serves HTML templates from `templates/`, static assets from `static/`, and a tiny JSON-backed image API under `/api/images`.
- templates/: All user-facing HTML (index, upload, gallery, view). Templates are mostly client-side JS heavy and expect two small SDKs at `/_sdk/data_sdk.js` and `/_sdk/element_sdk.js` which are included under `static/_sdk/`.
- static/uploads/: image files and `metadata.json` used as the persistent store for uploaded images. Each metadata entry has at least: `id`, `imageName`, `imageCategory`, `filename`, `uploadedAt`, `uploader`.

Key patterns & conventions

- Data flow: templates call `window.dataSdk.init(handler)` to obtain image lists and `dataSdk.create(obj)` to create images. The repository provides a minimal SDK implementation (static/_sdk) that proxies these calls to the Flask API:
  - GET `/api/images` -> returns list of metadata objects; each object includes `imageData` set to `/uploads/<filename>` (relative URL) for use as `img.src`.
  - POST `/api/images` -> accepts JSON payload with `imageData` as a data URL (base64), `imageName`, `imageCategory`, `id`, `uploadedAt` and saves the decoded file to `static/uploads/` then appends to `static/uploads/metadata.json`.
  - DELETE `/api/images/<id>` -> deletes metadata and underlying file if present.

- Templates expect image objects shaped like:
  - id: string
  - imageName: string
  - imageCategory: string
  - imageData: string (URL or data URL) — the SDK/API returns a relative URL for server-saved images
  - uploadedAt: ISO timestamp

Developer workflows (run & smoke tests)

1. Setup (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install flask
```

2. Run locally:

```powershell
python "c:\Users\pv\OneDrive\Máy tính\LTM\app.py"
# open http://127.0.0.1:5000
```

3. Smoke test (manual):
- Open Upload page (`/upload`) -> choose an image -> fill name/category -> submit. The client will send a data-URL JSON payload to `/api/images`. The server will save the file to `static/uploads/` and append an entry to `static/uploads/metadata.json`.
- Open Gallery (`/gallery`) -> images should appear; click an item to open detail view.

Project-specific tips & pitfalls

- `static/uploads/metadata.json` must be valid JSON (an array). If corrupted (for example contains Python code), the server will reset it to `[]` on load.
- The templates rely on `window.dataSdk` and `window.elementSdk`. If you change `app.py` endpoints, update `static/_sdk/data_sdk.js` accordingly.
- Templates use client-side base64 uploads (data URLs). The server decodes them and writes binary files; ensure `UPLOAD_FOLDER` is writable.
- IDs: the templates create `id` using Date.now().toString(); the server preserves this `id` in metadata and uses it for deletes.

Files to edit for common tasks

- Add/remove server-side logic: `app.py`
- Change UI (HTML/CSS/JS): `templates/*.html` and `static/css/styles.css`
- SDK behaviour (how templates talk to the server): `static/_sdk/data_sdk.js`, `static/_sdk/element_sdk.js`
- Persistent metadata: `static/uploads/metadata.json`

When modifying code, run these quick validations

- Start server and visit `/api/images` — should return valid JSON array.
- Upload a small image from `/upload`, then check `static/uploads/` contains a new file and `static/uploads/metadata.json` contains a new entry.
- From `/gallery`, ensure images load (image URLs are reachable at `/uploads/<filename>`).

If something is unclear

- If a template seems to expect a different field name, open that template and search for `.imageData`, `.imageName`, `dataSdk.create`, or `window.elementSdk` to see expectations.
- If uploads fail with JSON parsing errors, verify `static/uploads/metadata.json` is valid JSON and writable.

Please review this file and tell me if you want:
- stricter API validation and error codes
- migration from storing base64 payloads to multipart uploads
- or unit tests for `app.py` endpoints (I can add pytest tests).
