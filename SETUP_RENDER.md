# Deploy Guide to Render with GitHub

## Why Render Free?

✅ **$0/month** - Completely free  
✅ **Auto Deploy** - Every push = automatic deploy  
✅ **Auto Restart** - Wakes up automatically  
✅ **Zero maintenance** - Render handles everything  

**Limitations:**
- Service can sleep after 15 minutes
- But wakes up automatically when QBWC tries to connect
- Suitable for QBWC (runs once a day)

---

## Step 1: Create GitHub Private Repo

### 1.1 Create Repository

1. Go to [GitHub.com](https://github.com)
2. Click **+** → **New repository**
3. Settings:
   - **Repository name:** `qbwc-adapter` (or another name)
   - **Description:** `QuickBooks to Monday.com Adapter`
   - **Visibility:** **Private** ⭐ (Important!)
   - **Do NOT** check "Add README"
4. Click **Create repository**

### 1.2 Upload Files

**Option A: Via GitHub Web Interface**

1. On GitHub, click **uploading an existing file**
2. Drag and drop all files from `EN/`:
   - `app.py`
   - `qbwc_handler.py`
   - `xml_converter.py`
   - `n8n_client.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `.gitignore`
   - `.env.example` (optional)
3. Click **Commit changes**

**Option B: Via Git CLI**

```bash
cd EN
git init
git add .
git commit -m "Initial commit - QBWC Adapter"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/qbwc-adapter.git
git push -u origin main
```

---

## Step 2: Deploy to Render

### 2.1 Connect to GitHub

1. Go to [Render.com](https://render.com)
2. Click **Sign Up** and register (or **Log In**)
3. Click **New** → **Web Service**
4. Click **Connect GitHub**
5. **Authorize Render** - Give Render permissions to access GitHub
6. Select your repository: `qbwc-adapter`
7. Click **Connect**

### 2.2 Deploy Settings

1. **Name:** `qbwc-adapter` (or another name)
2. **Environment:** `Python 3` ⭐
3. **Plan:** **Free** ⭐ (Recommended - $0/month!)
4. **Region:** Select the closest one
5. **Branch:** `main` (or `master`)
6. **Root Directory:** (leave empty)
7. **Build Command:** `pip install -r requirements.txt`
8. **Start Command:** `gunicorn app:app`

### 2.3 Environment Variables

Click **Add Environment Variable** and add:

| Name | Value |
|------|-------|
| `QBWC_USER` | `admin` (or another name) |
| `QBWC_PASS` | `[strong password]` |
| `N8N_WEBHOOK_URL` | `[you'll get this from n8n later]` |
| `PORT` | `5000` |

**⚠️ Note:** You don't have `N8N_WEBHOOK_URL` yet - you'll get it after setting up n8n. You can update it later.

### 2.4 Create Service

1. Click **Create Web Service**
2. Wait for Deploy (2-3 minutes)
3. You'll get a URL like: `https://qbwc-adapter.onrender.com`

**Save this URL!** You'll need it for QBWC setup.

---

## Step 3: Health Check

Open in browser:
```
https://qbwc-adapter.onrender.com/health
```

Should see: `{"status": "ok"}`

If you see an error, check the Logs in Render.

---

## Step 4: Update N8N_WEBHOOK_URL

After you set up n8n and get the Webhook URL:

1. In Render, click on your Service
2. Click **Environment**
3. Click **Edit** next to `N8N_WEBHOOK_URL`
4. Update the value
5. Click **Save Changes**
6. Render will automatically redeploy

---

## Auto Deploy

From now on, every time you do `git push`:
1. Render will detect the change
2. Will automatically deploy
3. Service will work with the new code

**No need to do anything manually!**

---

## Troubleshooting

### Service not working?

1. Check the Logs in Render
2. Check that Environment Variables are correct
3. Check that `requirements.txt` is correct

### Service sleeping?

- This is normal on Render Free
- Service will wake up automatically when QBWC tries to connect
- If it takes too long, consider upgrading to Render Paid ($7/month)

---

**Ready! Now continue to `SETUP_N8N.md`**
