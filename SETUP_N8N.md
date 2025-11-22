# n8n Cloud Setup Guide

## Overview

This guide will walk you through setting up n8n Cloud to create a Workflow that receives data from the Python Adapter and uploads it to Monday.com.

---

## Step 1: Sign Up for n8n.io

### 1.1 Create Account

1. Go to [n8n.io](https://n8n.io)
2. Click **Sign Up**
3. Fill in details and register
4. Email verification (if required)

### 1.2 Choose Plan

**Recommended: Starter Plan ($20/month)**
- Enough for most uses
- Professional support
- Up to 5,000 Executions/month

---

## Step 2: Create Workflow

### 2.1 Create New Workflow

1. In n8n, click **Workflows** → **New Workflow**
2. Name the Workflow: `QuickBooks to Monday.com`

### 2.2 Add Webhook Node

1. Click **+** to add Node
2. Search for **Webhook** and add
3. Configure the Webhook:
   - **HTTP Method:** `POST`
   - **Path:** `qb-invoices`
   - **Response Mode:** `Respond When Last Node Finishes`
4. Click **Execute Node** to get the URL

### 2.3 Get Webhook URL

After Execute, you'll get a URL like:
```
https://your-instance.n8n.io/webhook/qb-invoices
```

**⚠️ Important:** Save this URL! You'll need it for Python Adapter setup.

---

## Step 3: Add Nodes for Data Processing

### 3.1 Set Node - Map Data

1. Add **Set** node
2. Connect it to Webhook
3. Configure Fields:

| Name | Value |
|------|-------|
| `invoice_number` | `={{ $json.data[0].ref_number }}` |
| `invoice_date` | `={{ $json.data[0].date }}` |
| `amount` | `={{ $json.data[0].total_amount }}` |
| `customer` | `={{ $json.data[0].customer }}` |
| `is_paid` | `={{ $json.data[0].is_paid }}` |
| `txn_id` | `={{ $json.data[0].txn_id }}` |

### 3.2 If Node - Check Data

1. Add **If** node
2. Connect it to Set
3. Set condition:
   - **Condition:** `{{ $json.data }}` exists

### 3.3 Monday.com Node - Create Item

1. Add **Monday.com** node
2. Connect it to If (True branch)
3. Configure:
   - **Authentication:** OAuth2 (connect Monday.com)
   - **Resource:** `Item`
   - **Operation:** `Create`
   - **Board ID:** `[Your Board ID from Monday.com]`
   - **Item Name:** `={{ $json.invoice_number }}`
   - **Column Values:** Configure according to your Board

### 3.4 Respond Node - Response

1. Add **Respond to Webhook** node
2. Connect it to Monday.com
3. Configure:
   - **Respond With:** `JSON`
   - **Response Body:** `={{ { "success": true, "invoice": $json.invoice_number } }}`

### 3.5 Error Handling

1. Add another **Respond to Webhook** node
2. Connect it to If (False branch)
3. Configure:
   - **Respond With:** `JSON`
   - **Response Body:** `={{ { "success": false, "error": "No data received" } }}`

---

## Step 4: Save and Activate

### 4.1 Save Workflow

1. Click **Save** (Ctrl+S)
2. Make sure Workflow is active (Active)

### 4.2 Test

1. Click **Execute Workflow** (or click Webhook Node)
2. Check that data is received correctly
3. Check that Monday.com receives the data

---

## Step 5: Update Python Adapter

Now update the Python Adapter with the Webhook URL:

1. In Render, click on your Service
2. Click **Environment**
3. Update `N8N_WEBHOOK_URL` with the URL you received
4. Render will automatically redeploy

---

## Troubleshooting

### Webhook not receiving data?

1. Check that Workflow is active (Active)
2. Check that Webhook URL is correct
3. Check the Logs in n8n

### Monday.com not receiving data?

1. Check that Authentication is correct
2. Check that Board ID is correct
3. Check the Column IDs

---

**Ready! Now continue to `SETUP_QBWC.md`**
