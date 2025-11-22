# Render Setup - Step by Step Guide

## Overview

You're on the Render dashboard. Follow these steps to deploy your Python Adapter.

---

## Step 1: Choose Service Type

On the "Create a new Service" page:

1. **Click on "Web Services"** card
   - It says: "Dynamic web app. Ideal for full-stack apps, API servers, and mobile backends."
   - Click the purple **"New Web Service →"** link

---

## Step 2: Connect to GitHub

### 2.1 First Time Setup

If this is your first time:

1. **Click "Connect GitHub"** button
2. **Authorize Render** - You'll be redirected to GitHub
3. **Click "Authorize Render"** on GitHub
4. You'll be redirected back to Render

### 2.2 Select Repository

1. **Search for your repository** (e.g., `qbwc-adapter`)
2. **Click on it** to select
3. **Click "Connect"**

**⚠️ Don't have a GitHub repo yet?** See "Step 0" below.

---

## Step 3: Configure Service

After connecting to GitHub, you'll see configuration options:

### 3.1 Basic Settings

| Field | Value | Notes |
|-------|-------|-------|
| **Name** | `qbwc-adapter` | Or any name you want |
| **Environment** | `Python 3` | ⭐ Must be Python 3 |
| **Region** | Choose closest | e.g., Frankfurt, Oregon |
| **Branch** | `main` | Or `master` if that's your branch |
| **Root Directory** | (leave empty) | ⭐ Leave empty! |

### 3.2 Plan

- **Select: Free** ⭐
  - $0/month
  - Service may sleep after 15 minutes (but wakes up automatically)
  - Perfect for QBWC (runs once a day)

### 3.3 Build & Start Commands

| Field | Value |
|-------|-------|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

---

## Step 4: Environment Variables

**⚠️ Important:** Add these BEFORE clicking "Create Web Service"!

Click **"Add Environment Variable"** and add each one:

### Required Variables:

| Name | Value | Where to Find |
|------|-------|---------------|
| `QBWC_USER` | `admin` | From your `.env` file (or what you set in installer) |
| `QBWC_PASS` | `your_password` | From your `.env` file (the password you set) |
| `PORT` | `5000` | Always `5000` |
| `N8N_WEBHOOK_URL` | `https://...` | You'll get this from n8n later (can update later) |

**For now, use a placeholder for `N8N_WEBHOOK_URL`:**
```
https://your-n8n-instance.com/webhook/qb-invoices
```

You can update it later after setting up n8n.

---

## Step 5: Create Service

1. **Review all settings**
2. **Click "Create Web Service"** (bottom right)
3. **Wait 2-3 minutes** for deployment

You'll see:
- Build logs
- Deploy progress
- Final status

---

## Step 6: Get Your URL

After deployment completes:

1. **Copy the URL** at the top (e.g., `https://qbwc-adapter.onrender.com`)
2. **Save it!** You'll need it for:
   - Updating `.qwc` file
   - Testing the service

---

## Step 7: Test the Service

1. **Open in browser:**
   ```
   https://your-service-name.onrender.com/health
   ```

2. **Should see:**
   ```json
   {"status": "ok"}
   ```

3. **If you see an error:**
   - Check the **Logs** tab in Render
   - Verify Environment Variables are correct
   - Check that all files were uploaded to GitHub

---

## Step 0: Upload Files to GitHub (If Not Done Yet)

If you don't have a GitHub repository yet:

### Option A: Using GitHub Web Interface (Easiest)

1. **Go to [GitHub.com](https://github.com)**
2. **Click "+" → "New repository"**
3. **Settings:**
   - Name: `qbwc-adapter`
   - Description: `QuickBooks to Monday.com Adapter`
   - **Visibility: Private** ⭐
   - **Don't check "Add README"**
4. **Click "Create repository"**

5. **On the next page, click "uploading an existing file"**

6. **Drag and drop these files** (from `EN/` directory):
   - ✅ `app.py`
   - ✅ `qbwc_handler.py`
   - ✅ `xml_converter.py`
   - ✅ `n8n_client.py`
   - ✅ `utils.py`
   - ✅ `requirements.txt`
   - ✅ `Procfile`
   - ✅ `runtime.txt`
   - ✅ `.gitignore`
   - ✅ `.env.example` (optional)

7. **Click "Commit changes"**

### Option B: Using Git CLI

If you already have Git set up:

```powershell
cd C:\Users\dor\Downloads\iperf3.1.1_32  # Or wherever your files are
git init
git add app.py qbwc_handler.py xml_converter.py n8n_client.py utils.py requirements.txt Procfile runtime.txt .gitignore
git commit -m "Initial commit - QBWC Adapter"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/qbwc-adapter.git
git push -u origin main
```

---

## Required Files Checklist

Make sure these files are in your GitHub repository:

- [ ] `app.py` - Main Flask application
- [ ] `qbwc_handler.py` - QBWC protocol handler
- [ ] `xml_converter.py` - XML to JSON converter
- [ ] `n8n_client.py` - n8n webhook client
- [ ] `utils.py` - Utility functions
- [ ] `requirements.txt` - Python dependencies
- [ ] `Procfile` - Render start command
- [ ] `runtime.txt` - Python version
- [ ] `.gitignore` - Git ignore rules

**⚠️ Don't upload `.env` file!** It contains secrets. Use Environment Variables in Render instead.

---

## After Deployment

### Update .qwc File

1. **Open `qb-adapter.qwc`** in a text editor
2. **Update the URL:**
   ```xml
   <AppURL>https://your-service-name.onrender.com/qbwc</AppURL>
   ```
3. **Save the file**

### Test with QBWC

1. **Open QuickBooks Desktop** (must be open!)
2. **Open QuickBooks Web Connector**
3. **Add the updated `.qwc` file**
4. **Test the connection**

---

## Troubleshooting

### "Build failed" error?

- Check that `requirements.txt` exists and is correct
- Check that `Procfile` exists and has: `web: gunicorn app:app`
- Check the Logs tab for specific error messages

### "Service not responding" error?

- Check Environment Variables are set correctly
- Check that `PORT=5000` is set
- Check the Logs tab for errors

### "Cannot connect" from QBWC?

- Make sure the service is deployed (check Render dashboard)
- Verify the URL in `.qwc` file matches your Render URL
- Test the `/health` endpoint in browser first

---

## Next Steps

After successful deployment:

1. ✅ **Update `.qwc` file** with Render URL
2. ✅ **Set up n8n workflow** (see `SETUP_N8N.md`)
3. ✅ **Update `N8N_WEBHOOK_URL`** in Render Environment Variables
4. ✅ **Test with QBWC**

---

**Ready! Your service is now live on Render! 🚀**

