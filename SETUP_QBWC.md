# QuickBooks Web Connector Setup Guide

## Overview

This guide will walk you through installing and configuring QuickBooks Web Connector (QBWC) to connect to the Python Adapter.

---

## Step 1: Install QuickBooks Web Connector

### 1.1 Download

1. Go to [Intuit Developer](https://developer.intuit.com/app/developer/qbwc/docs/get-started/get-started-with-quickbooks-web-connector)
2. Download QuickBooks Web Connector
3. Install the software

### 1.2 Open QBWC

1. Open QuickBooks Web Connector
2. If this is the first time, you'll need to configure QuickBooks Desktop

---

## Step 2: Create .qwc File

### 2.1 Create XML File

Create a new file named `qb-adapter.qwc` with the following content:

```xml
<?xml version="1.0"?>
<QBWCXML>
  <AppName>QB to Monday Adapter</AppName>
  <AppID></AppID>
  <AppURL>https://qbwc-adapter.onrender.com/qbwc</AppURL>
  <AppDescription>Sync QuickBooks invoices to Monday.com</AppDescription>
  <AppSupport>https://qbwc-adapter.onrender.com</AppSupport>
  <UserName>admin</UserName>
  <OwnerID>{GENERATE-GUID}</OwnerID>
  <FileID>{GENERATE-GUID}</FileID>
  <QBType>QBFS</QBType>
  <Scheduler>
    <RunEveryNMinutes>1440</RunEveryNMinutes>
  </Scheduler>
</QBWCXML>
```

### 2.2 Replace Values

**Replace:**
- `AppURL` → Your Python Adapter URL (from Render)
- `UserName` → Same name as in `QBWC_USER` (in Render Environment Variables)
- `OwnerID` → New GUID (generate at: https://www.guidgenerator.com/)
- `FileID` → Another new GUID
- `RunEveryNMinutes` → `1440` (once a day) or another number of minutes

### 2.3 Save File

Save the file as `qb-adapter.qwc` in an accessible location.

---

## Step 3: Add to QBWC

### 3.1 Add Application

1. In QBWC, click **Add an Application**
2. Select the file `qb-adapter.qwc`
3. Click **Next**

### 3.2 Configure Authentication

1. Enter Username: `admin` (or what you set in Render)
2. Enter Password: `[password you set in Render]`
3. Click **Next**

### 3.3 Configure QuickBooks Company File

1. Select your QuickBooks Company file
2. Click **Next**
3. Click **Finish**

---

## Step 4: Configure Schedule

### 4.1 Automatic Schedule

In QBWC, you can configure:
- **Run Every N Minutes:** Number of minutes between runs
- **Run on Weekdays Only:** Only on weekdays
- **Run on Specific Days:** Specific days

**Recommended:** Once a day (1440 minutes) at a fixed time.

### 4.2 Manual Run

You can always run manually:
1. Select the Application
2. Click **Update Selected**

---

## Step 5: Test

### 5.1 Test Connection

1. In QBWC, select the Application
2. Click **Update Selected**
3. Check the Log:
   - ✅ **Success** = Everything works
   - ❌ **Error** = Check the Logs

### 5.2 Check Data

1. Check in n8n that Webhook received data
2. Check in Monday.com that a new Item was created

---

## Troubleshooting

### QBWC not connecting?

1. Check that URL is correct (in `.qwc` file)
2. Check that Username/Password are correct
3. Check that Python Adapter is running (in Render)
4. Check the Logs in Render

### QBWC connects but no data?

1. Check that QuickBooks Desktop is open
2. Check that there are invoices in QuickBooks
3. Check the Logs in Render

### Errors in QBWC?

1. Check the Log in QBWC
2. Check the Logs in Render
3. Check the Logs in n8n

---

## Important Notes

### QuickBooks Desktop Must Be Open

QBWC can only connect when QuickBooks Desktop is open. If the computer is turned off, you'll need to turn it on and start QuickBooks.

### Schedule

If the computer is turned off at night, QBWC won't run. Make sure the computer is on at the time you configured.

---

**Ready! The integration should work! 🎉**
