# Testing Guide - QuickBooks to Monday.com Integration

## Overview
This guide will help you test the complete integration from QuickBooks Desktop to Monday.com via n8n.

---

## Prerequisites Checklist

Before starting, make sure you have:
- ✅ QuickBooks Desktop installed and running
- ✅ n8n account set up (cloud or self-hosted)
- ✅ Monday.com account (for receiving data)
- ✅ Python Adapter deployed to Render (or running locally)
- ✅ QuickBooks Web Connector installed

---

## Step 1: Run the GUI Installer

1. Open PowerShell
2. Navigate to the project directory:
   ```powershell
   cd C:\Users\dor\automations\GTO\EN
   ```
3. Run the installer:
   ```powershell
   .\install-gui.ps1
   ```
4. Fill in all required fields:
   - **QBWC Tab**: Username and Password
   - **n8n Tab**: Your n8n webhook URL
   - **Render Tab**: Service name (or use local testing)
   - **GitHub Tab**: (Optional) Your GitHub details
5. Click **"Preview Files"** to verify configuration
6. Click **"Install"** to generate files

---

## Step 2: Set Up n8n Workflow

### 2.1 Create Webhook Node

1. Go to your n8n instance
2. Create a new workflow
3. Add a **Webhook** node:
   - **Method**: POST
   - **Path**: `qb-invoices` (or any path you prefer)
   - **Response Mode**: Respond When Last Node Finishes
4. Click **"Listen for Test Event"** to get your webhook URL
5. Copy the webhook URL (e.g., `https://your-n8n-instance.com/webhook/qb-invoices`)

### 2.2 Add Monday.com Node

1. Add a **Monday.com** node after the Webhook
2. Configure Monday.com credentials:
   - Add your Monday.com API token
   - Select your board
   - Select your group
3. Configure the node:
   - **Operation**: Create Item
   - **Board ID**: Your Monday.com board ID
   - **Group ID**: Your group ID
   - **Item Name**: Map from webhook data (e.g., `{{ $json.invoice.RefNumber }}`)
   - **Column Values**: Map relevant fields:
     - Invoice Number: `{{ $json.invoice.RefNumber }}`
     - Customer: `{{ $json.invoice.CustomerRef.FullName }}`
     - Amount: `{{ $json.invoice.TotalAmount }}`
     - Date: `{{ $json.invoice.TxnDate }}`

### 2.3 Test the Webhook

1. Click **"Execute Workflow"** in n8n
2. Use the webhook URL to send a test request:
   ```powershell
   $testData = @{
       invoice = @{
           RefNumber = "TEST-001"
           CustomerRef = @{
               FullName = "Test Customer"
           }
           TotalAmount = 100.00
           TxnDate = "2024-01-15"
       }
   } | ConvertTo-Json -Depth 10
   
   Invoke-RestMethod -Uri "YOUR_N8N_WEBHOOK_URL" -Method Post -Body $testData -ContentType "application/json"
   ```
3. Verify the item appears in Monday.com

### 2.4 Activate the Workflow

1. Click **"Active"** toggle to activate the workflow
2. The webhook is now ready to receive data

---

## Step 3: Deploy Python Adapter

### Option A: Deploy to Render (Recommended)

1. Go to https://render.com
2. Sign up / Log in
3. Click **"New"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name**: Your service name (from installer)
   - **Environment**: Python 3
   - **Plan**: Free
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Add Environment Variables:
   - `QBWC_USER`: Your QBWC username
   - `QBWC_PASS`: Your QBWC password
   - `N8N_WEBHOOK_URL`: Your n8n webhook URL
   - `PORT`: `5000`
7. Click **"Create Web Service"**
8. Wait for deployment (2-3 minutes)
9. Copy the service URL (e.g., `https://your-service.onrender.com`)

### Option B: Run Locally (For Testing)

1. Open PowerShell in the `EN/` directory
2. Create virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Create `.env` file (or use the one from installer):
   ```
   QBWC_USER=admin
   QBWC_PASS=your_password
   N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/qb-invoices
   PORT=5000
   DEBUG=True
   ```
5. Run the adapter:
   ```powershell
   python app.py
   ```
6. The adapter will run on `http://localhost:5000`

---

## Step 4: Update QBWC Configuration File

1. Open `qb-adapter.qwc` in a text editor
2. Update the `<AppURL>` tag with your Render URL or local URL:
   ```xml
   <AppURL>https://your-service.onrender.com/qbwc</AppURL>
   ```
   Or for local testing:
   ```xml
   <AppURL>http://localhost:5000/qbwc</AppURL>
   ```
3. Save the file

---

## Step 5: Configure QuickBooks Web Connector

1. Download and install QBWC from:
   https://developer.intuit.com/app/developer/qbwc/docs/get-started/get-started-with-quickbooks-web-connector

2. Open QuickBooks Desktop
3. Open QuickBooks Web Connector
4. Click **"Add an Application"**
5. Select the `qb-adapter.qwc` file
6. Enter:
   - **Username**: Your QBWC username (from installer)
   - **Password**: Your QBWC password
7. Click **"OK"**
8. The application should appear in the list
9. Click **"Update"** to test the connection

---

## Step 6: Create Test Data in QuickBooks

### 6.1 Create a Test Customer

1. In QuickBooks, go to **Customers** → **Customer Center**
2. Click **"New Customer"**
3. Fill in:
   - **Customer Name**: "Test Customer"
   - **Company Name**: "Test Company"
   - **Email**: test@example.com
4. Click **"OK"**

### 6.2 Create a Test Invoice

1. In QuickBooks, go to **Customers** → **Create Invoices**
2. Select the test customer
3. Add items:
   - **Item**: Select or create a test item
   - **Quantity**: 1
   - **Rate**: 100.00
4. Fill in:
   - **Invoice #**: "TEST-001"
   - **Date**: Today's date
5. Click **"Save & Close"**

### 6.3 Create Multiple Test Invoices (Optional)

Create 3-5 test invoices with different:
- Customers
- Amounts
- Dates
- Invoice numbers

This will help test the integration with multiple records.

---

## Step 7: Test the Integration

### 7.1 Manual Test (QBWC)

1. Make sure QuickBooks Desktop is open
2. Open QuickBooks Web Connector
3. Click **"Update"** next to your application
4. Watch the logs in QBWC for:
   - Connection successful
   - Data sent
   - Response received

### 7.2 Check Python Adapter Logs

If running locally, check the PowerShell window for:
- `INFO: Received QBWC request`
- `INFO: Processing invoice data`
- `INFO: Sending to n8n: ...`
- `INFO: Response from n8n: ...`

If on Render, check the Render logs:
1. Go to Render dashboard
2. Click on your service
3. Go to **"Logs"** tab
4. Look for similar messages

### 7.3 Check n8n Workflow

1. Go to your n8n workflow
2. Check the **"Executions"** tab
3. You should see:
   - Successful executions
   - Data received from webhook
   - Items created in Monday.com

### 7.4 Verify Monday.com

1. Go to your Monday.com board
2. Check for new items:
   - Should have invoice data
   - Customer names
   - Amounts
   - Dates

---

## Step 8: Troubleshooting

### Issue: QBWC Can't Connect

**Symptoms**: Error in QBWC, connection failed

**Solutions**:
- Check if Python Adapter is running (Render or local)
- Verify the URL in `qb-adapter.qwc` is correct
- Check firewall settings
- For local testing, ensure `http://localhost:5000` is accessible

### Issue: No Data in n8n

**Symptoms**: n8n workflow not receiving data

**Solutions**:
- Check Python Adapter logs for errors
- Verify `N8N_WEBHOOK_URL` in `.env` is correct
- Test n8n webhook manually (see Step 2.3)
- Check n8n workflow is activated

### Issue: Data Not Appearing in Monday.com

**Symptoms**: n8n receives data but Monday.com doesn't

**Solutions**:
- Check Monday.com node configuration
- Verify Monday.com API token is valid
- Check column mappings in n8n
- Test Monday.com connection in n8n

### Issue: Wrong Data Format

**Symptoms**: Data appears but fields are wrong

**Solutions**:
- Check n8n node mappings
- Verify QuickBooks data structure
- Check Python Adapter XML to JSON conversion
- Review `xml_converter.py` for field mappings

---

## Step 9: Schedule Automatic Updates

Once testing is successful:

1. In QuickBooks Web Connector, click on your application
2. Click **"Schedule"**
3. Set schedule:
   - **Frequency**: Daily (recommended)
   - **Time**: Choose a time when QuickBooks is usually open
4. Click **"OK"**

Now the integration will run automatically!

---

## Test Data Summary

For comprehensive testing, create:

- ✅ 3-5 test customers
- ✅ 5-10 test invoices
- ✅ Different invoice amounts
- ✅ Different dates
- ✅ Different customers

This will help verify:
- Multiple records processing
- Data accuracy
- Error handling
- Performance

---

## Next Steps

After successful testing:

1. ✅ Remove test data from QuickBooks (optional)
2. ✅ Clean up test items in Monday.com (optional)
3. ✅ Set up production schedule in QBWC
4. ✅ Monitor logs for first few days
5. ✅ Document any customizations

---

## Support

If you encounter issues:
- Check the logs (Python Adapter, n8n, QBWC)
- Review the documentation files
- Verify all configuration settings
- Test each component individually

Good luck with your testing! 🚀

