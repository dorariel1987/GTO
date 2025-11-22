# QuickBooks Desktop → Monday.com Integration

## Solution: Python Adapter + n8n Cloud + Render Free

Full automatic integration between QuickBooks Desktop and Monday.com using:
- **Python Adapter** - Runs on Render (Free tier)
- **n8n Cloud** - Workflow automation
- **QuickBooks Web Connector** - Connection to QuickBooks Desktop

---

## 🚀 Quick Start

### Option 1: Automated Installation (Recommended!) ⭐⭐⭐

**Windows Installer Script:**
```powershell
.\install.ps1
```

The script will:
- ✅ Create `.env` file
- ✅ Create `.qwc` file
- ✅ Set up Git repository
- ✅ Create GitHub repository (optional)
- ✅ Detailed instructions for each step

**See:** [`INSTALLER_GUIDE.md`](INSTALLER_GUIDE.md) - Detailed guide

### Option 2: Manual Installation

**⭐ Start here:** [`QUICK_START.md`](QUICK_START.md) - Practical step-by-step guide

### 1. Deploy Python Adapter to Render

**See:** [`SETUP_RENDER.md`](SETUP_RENDER.md) - Detailed guide

**Quick steps:**
1. Create GitHub Private Repo
2. Upload all files from `EN/`
3. Connect to Render
4. Select **Free tier** ($0/month)
5. Configure Environment Variables
6. Deploy!

### 2. Configure n8n Cloud

**See:** [`SETUP_N8N.md`](SETUP_N8N.md) - Detailed guide

**Quick steps:**
1. Sign up for n8n.io
2. Create Workflow with Webhook
3. Add Monday.com node
4. Save Webhook URL

### 3. Configure QuickBooks Web Connector

**See:** [`SETUP_QBWC.md`](SETUP_QBWC.md) - Detailed guide

**Quick steps:**
1. Install QBWC
2. Create `.qwc` file
3. Add to QBWC
4. Set schedule

---

## 📁 Project Structure

```
EN/
├── app.py                  # Flask application (main)
├── qbwc_handler.py         # QBWC protocol handler
├── xml_converter.py        # XML to JSON converter
├── n8n_client.py           # n8n webhook client
├── requirements.txt        # Python dependencies
├── Procfile               # Render start command
├── runtime.txt            # Python version
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── n8n_workflow.json      # n8n workflow (import)
├── README.md              # This file
├── SETUP_RENDER.md        # Render Deploy guide
├── SETUP_N8N.md           # n8n setup guide
├── SETUP_QBWC.md          # QBWC setup guide
└── SOLUTION.md            # Solution explanation
```

---

## 💰 Costs

**Monthly:**
- **Render:** $0/month (Free tier) ⭐
- **n8n Cloud:** $20/month (Starter plan)
- **Total:** $20/month

**Maintenance:** Zero - Everything is cloud-managed!

**Note about Render Free:**
- Service can sleep after 15 minutes
- But wakes up automatically when QBWC tries to connect
- Suitable for QBWC (runs once a day)

---

## 🔧 Environment Variables

Create `.env` file (or configure in Render):

```env
# QuickBooks Web Connector Authentication
QBWC_USER=admin
QBWC_PASS=your_secure_password_here

# n8n Configuration
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/qb-invoices
N8N_TIMEOUT=30
N8N_MAX_RETRIES=3
N8N_RETRY_DELAY=2

# Server Configuration
PORT=5000
DEBUG=False
```

**See:** `.env.example` for example

**Important:** `QBWC_PASS` and `N8N_WEBHOOK_URL` are required!

---

## 📚 Guides

### Deploy:
- **`SETUP_RENDER.md`** ⭐ - Deploy to Render with GitHub (Auto Deploy)

### Setup:
- **`SETUP_N8N.md`** - n8n Cloud setup
- **`SETUP_QBWC.md`** - QuickBooks Web Connector setup

### Explanation:
- **`SOLUTION.md`** - Detailed solution explanation
- **`FUTURE_EXTENSIONS.md`** - Future extensions
- **`SOLUTION_REVIEW.md`** - Solution review and best practices
- **`IMPROVEMENTS_SUMMARY.md`** - Improvements summary
- **`PRODUCTION_READY.md`** ⭐ - Production Ready summary
- **`CHANGELOG.md`** - List of changes

---

## ✅ What Does the Client Need?

**Nothing!**

- Client doesn't need to know Git
- Client doesn't need to know Python
- Client only receives URL: `https://qb-adapter.onrender.com`
- Maintenance: Zero

---

## 🎯 How It Works?

```
QuickBooks Desktop
    │
    ▼
QuickBooks Web Connector (QBWC)
    │ - Runs once a day (schedule)
    │
    ▼
Python Adapter (Render Free)
    │ - Wakes up automatically
    │ - Processes QBWC protocol
    │ - Converts QBXML → JSON
    │
    ▼
n8n Cloud
    │ - Workflow automation
    │ - All logic here
    │
    ▼
Monday.com
```

---

## 📝 Notes

- All files are written in English
- Solution: **Python + n8n Cloud + Render Free**
- Deploy: **GitHub Private Repo + Render**

---

**Updated:** 2025  
**Status:** Ready for implementation - Production Ready  
**Version:** 1.1.0

**See:** `CHANGELOG.md` for list of improvements
