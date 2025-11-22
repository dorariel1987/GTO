# GitHub Files Checklist - What to Upload

## ✅ Required Files (Must Upload)

These files are **essential** for the service to work on Render:

### Python Code Files:
- [ ] `app.py` - Main Flask application
- [ ] `qbwc_handler.py` - QBWC protocol handler
- [ ] `xml_converter.py` - XML to JSON converter
- [ ] `n8n_client.py` - n8n webhook client
- [ ] `utils.py` - Utility functions

### Configuration Files:
- [ ] `requirements.txt` - Python dependencies (Flask, gunicorn, etc.)
- [ ] `Procfile` - Render start command (`web: gunicorn app:app`)
- [ ] `runtime.txt` - Python version (e.g., `python-3.11.0`)
- [ ] `.gitignore` - Git ignore rules

---

## 📚 Recommended Files (Documentation)

These files are helpful but not required:

### Setup Guides:
- [ ] `README.md` - Project overview
- [ ] `SETUP_RENDER.md` - Render deployment guide
- [ ] `SETUP_N8N.md` - n8n setup guide
- [ ] `SETUP_QBWC.md` - QBWC setup guide
- [ ] `RENDER_STEP_BY_STEP.md` - Detailed Render guide
- [ ] `QUICK_START.md` - Quick start guide
- [ ] `TESTING_GUIDE.md` - Testing instructions
- [ ] `QUICK_TEST_CHECKLIST.md` - Test checklist

### Other Documentation:
- [ ] `CHANGELOG.md` - Version history
- [ ] `PRODUCTION_READY.md` - Production readiness info
- [ ] `IMPROVEMENTS_SUMMARY.md` - Improvements made

---

## ⚠️ DO NOT Upload (Secrets & Temporary Files)

**Never upload these files!** They contain secrets or are temporary:

### Secrets:
- [ ] ❌ `.env` - Contains passwords and API keys
- [ ] ❌ `qb-adapter.qwc` - Contains your specific configuration (if it has secrets)

### Temporary/Generated Files:
- [ ] ❌ `__pycache__/` - Python cache (auto-generated)
- [ ] ❌ `venv/` or `env/` - Virtual environment (auto-generated)
- [ ] ❌ `*.pyc` - Compiled Python files (auto-generated)
- [ ] ❌ `*.log` - Log files

### Local Testing Files:
- [ ] ❌ `qb-adapter-local.qwc` - Local testing file
- [ ] ❌ `test_data.iif` - Test data (optional, can upload if you want)
- [ ] ❌ `install.ps1` - Windows installer (not needed on Render)
- [ ] ❌ `install-gui.ps1` - GUI installer (not needed on Render)

---

## 📋 Quick Upload Checklist

### Minimum Required (Service will work):
```
✅ app.py
✅ qbwc_handler.py
✅ xml_converter.py
✅ n8n_client.py
✅ utils.py
✅ requirements.txt
✅ Procfile
✅ runtime.txt
✅ .gitignore
```

### Recommended (With documentation):
```
✅ All files above, plus:
✅ README.md
✅ SETUP_RENDER.md
✅ SETUP_N8N.md
✅ SETUP_QBWC.md
```

---

## 🔒 Security Notes

### Why not upload `.env`?

The `.env` file contains:
- `QBWC_PASS` - Your password
- `N8N_WEBHOOK_URL` - Your n8n webhook URL
- Other sensitive information

**Instead:** Use Render's **Environment Variables** feature to set these values securely.

### What about `.qwc` file?

The `.qwc` file contains:
- Your Render URL
- Your username
- GUIDs specific to your setup

**You can upload it** if you want, but it's not required for Render. It's only needed locally for QBWC setup.

---

## 📤 How to Upload

### Option 1: GitHub Web Interface (Easiest)

1. Go to your GitHub repository
2. Click **"uploading an existing file"**
3. **Drag and drop** all required files
4. Click **"Commit changes"**

### Option 2: Git CLI

```powershell
cd EN  # Or wherever your files are
git add app.py qbwc_handler.py xml_converter.py n8n_client.py utils.py requirements.txt Procfile runtime.txt .gitignore README.md
git commit -m "Initial commit - QBWC Adapter"
git push
```

---

## ✅ Verification

After uploading, verify:

1. **All required files are in the repository**
2. **`.env` file is NOT in the repository** (check `.gitignore` is working)
3. **`requirements.txt` has all dependencies**
4. **`Procfile` has correct start command**

---

## 🚀 Next Steps

After uploading to GitHub:

1. ✅ Connect GitHub to Render
2. ✅ Set Environment Variables in Render
3. ✅ Deploy!

See `RENDER_STEP_BY_STEP.md` for detailed deployment instructions.

