# Quick Start - Practical Steps

## What to Do Now?

### Step 1: Deploy Python Adapter to Render ⭐

**Estimated time:** 15-20 minutes

1. **Create GitHub Private Repo**
   - Go to [GitHub.com](https://github.com)
   - Create new Repository (Private)
   - Upload all files from `EN/`

2. **Deploy to Render**
   - Go to [Render.com](https://render.com)
   - Create new Web Service
   - Connect to GitHub Repo
   - Select **Free tier**
   - Configure Environment Variables:
     - `QBWC_USER=admin`
     - `QBWC_PASS=[strong password]`
     - `N8N_WEBHOOK_URL=[update later]`
     - `PORT=5000`

3. **Get the URL**
   - You'll get a URL like: `https://qbwc-adapter.onrender.com`
   - Test: `https://qbwc-adapter.onrender.com/health`
   - Should see: `{"status": "ok"}`

**See:** `SETUP_RENDER.md` for detailed guide

---

### Step 2: Configure n8n Cloud ⭐

**Estimated time:** 10-15 minutes

1. **Sign up for n8n**
   - Go to [n8n.io](https://n8n.io)
   - Sign up (Starter plan - $20/month)

2. **Create Workflow**
   - Create new Workflow
   - Add Webhook Node
   - Get the Webhook URL

3. **Add Monday.com Node**
   - Connect Monday.com
   - Configure Board ID
   - Save the Workflow

4. **Update Render**
   - Go back to Render
   - Update `N8N_WEBHOOK_URL` with the URL you received

**See:** `SETUP_N8N.md` for detailed guide

---

### Step 3: Configure QuickBooks Web Connector ⭐

**Estimated time:** 10-15 minutes

1. **Install QBWC**
   - Download from [Intuit Developer](https://developer.intuit.com/app/developer/qbwc/docs/get-started/get-started-with-quickbooks-web-connector)
   - Install the software

2. **Create .qwc file**
   - Create `qb-adapter.qwc` file
   - Replace URL in `AppURL` (from Render)
   - Generate new GUIDs

3. **Add to QBWC**
   - Open QBWC
   - Add the `.qwc` file
   - Enter Username/Password (same as in Render)

4. **Configure schedule**
   - Once a day (1440 minutes)
   - Or run manually

**See:** `SETUP_QBWC.md` for detailed guide

---

### Step 4: Test ⭐

**Estimated time:** 5 minutes

1. **Run manually**
   - In QBWC, click **Update Selected**
   - Check the Log

2. **Check in n8n**
   - Open the Workflow
   - Check that Webhook received data

3. **Check in Monday.com**
   - Open the Board
   - Check that a new Item was created

---

## Recommended Work Order

1. ✅ **Step 1** - Deploy to Render (most important!)
2. ✅ **Step 2** - Configure n8n
3. ✅ **Step 3** - Configure QBWC
4. ✅ **Step 4** - Test

---

## What If Something Doesn't Work?

### Render not working?
- Check the Logs in Render
- Check that Environment Variables are correct
- Check that `requirements.txt` is correct

### n8n not receiving data?
- Check that Workflow is active
- Check that Webhook URL is correct
- Check the Logs in n8n

### QBWC not connecting?
- Check that URL is correct (in `.qwc` file)
- Check that Username/Password are correct
- Check that QuickBooks Desktop is open

---

## Important Files

- **`SETUP_RENDER.md`** - Detailed Render guide
- **`SETUP_N8N.md`** - Detailed n8n guide
- **`SETUP_QBWC.md`** - Detailed QBWC guide
- **`SOLUTION.md`** - Solution explanation

---

**Ready to start? Begin with `SETUP_RENDER.md`! 🚀**

