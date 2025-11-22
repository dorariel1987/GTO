# Quick Test Checklist - QuickBooks to Monday.com Integration

## Pre-Test Setup (5 minutes)

- [ ] QuickBooks Desktop installed and running
- [ ] n8n workflow created and activated
- [ ] Python Adapter running (Render or local)
- [ ] QuickBooks Web Connector installed
- [ ] QBWC configured with `.qwc` file
- [ ] Test data loaded into QuickBooks (use `test_data.iif`)

---

## Step 1: Load Test Data (2 minutes)

1. [ ] Open QuickBooks Desktop
2. [ ] Go to **File** → **Utilities** → **Import** → **IIF Files**
3. [ ] Select `test_data.iif`
4. [ ] Click **Import**
5. [ ] Verify data imported:
   - [ ] 5 customers created
   - [ ] 3 items created
   - [ ] 5 invoices created

---

## Step 2: Verify n8n Workflow (1 minute)

1. [ ] Open n8n workflow
2. [ ] Check workflow is **Active**
3. [ ] Verify webhook URL is correct
4. [ ] Test webhook manually (optional):
   ```powershell
   $test = @{invoice=@{RefNumber="TEST";TotalAmount=100}} | ConvertTo-Json
   Invoke-RestMethod -Uri "YOUR_WEBHOOK_URL" -Method Post -Body $test -ContentType "application/json"
   ```

---

## Step 3: Verify Python Adapter (1 minute)

1. [ ] Check adapter is running:
   - Local: PowerShell window shows "Running on http://localhost:5000"
   - Render: Check dashboard shows "Live"
2. [ ] Test health endpoint:
   - Open: `http://localhost:5000/health` (or Render URL)
   - Should see: `{"status": "ok"}`

---

## Step 4: Run QBWC Test (2 minutes)

1. [ ] Make sure QuickBooks Desktop is **open**
2. [ ] Open QuickBooks Web Connector
3. [ ] Select your application
4. [ ] Click **"Update Selected"**
5. [ ] Watch the log:
   - [ ] ✅ Connection successful
   - [ ] ✅ Authentication successful
   - [ ] ✅ Data sent
   - [ ] ✅ Response received

---

## Step 5: Verify Data Flow (3 minutes)

### Check Python Adapter Logs
- [ ] Log shows: "Received QBWC request"
- [ ] Log shows: "Processing invoice data"
- [ ] Log shows: "Sending to n8n: ..."
- [ ] Log shows: "Response from n8n: ..."

### Check n8n Executions
- [ ] Go to n8n workflow → **Executions** tab
- [ ] See new execution(s)
- [ ] Execution status: **Success**
- [ ] Data received in webhook node

### Check Monday.com
- [ ] Open your Monday.com board
- [ ] See new items created
- [ ] Items have correct data:
  - [ ] Invoice numbers
  - [ ] Customer names
  - [ ] Amounts
  - [ ] Dates

---

## Step 6: Verify Data Accuracy (2 minutes)

Check that data in Monday.com matches QuickBooks:

| QuickBooks Invoice | Monday.com Item | Match? |
|-------------------|-----------------|--------|
| INV-001 | INV-001 | [ ] |
| INV-002 | INV-002 | [ ] |
| INV-003 | INV-003 | [ ] |
| INV-004 | INV-004 | [ ] |
| INV-005 | INV-005 | [ ] |

Check amounts:
- [ ] Invoice amounts match
- [ ] Customer names match
- [ ] Dates match

---

## Troubleshooting Quick Reference

### QBWC Can't Connect
- [ ] Check Python Adapter is running
- [ ] Check URL in `.qwc` file is correct
- [ ] Check Username/Password match
- [ ] Check QuickBooks Desktop is open

### No Data in n8n
- [ ] Check Python Adapter logs for errors
- [ ] Check `N8N_WEBHOOK_URL` in `.env` is correct
- [ ] Check n8n workflow is active
- [ ] Test webhook manually

### Data Not in Monday.com
- [ ] Check n8n execution logs
- [ ] Check Monday.com node configuration
- [ ] Check Monday.com API token
- [ ] Check column mappings

---

## Success Criteria ✅

All of these should be true:
- [ ] QBWC connects successfully
- [ ] Python Adapter processes data
- [ ] n8n receives data
- [ ] Monday.com items created
- [ ] Data is accurate
- [ ] All 5 test invoices synced

---

## Next Steps After Successful Test

1. [ ] Remove test data (optional)
2. [ ] Set up production schedule in QBWC
3. [ ] Monitor logs for first few days
4. [ ] Document any customizations

---

**Total Test Time: ~15 minutes**

**Status:** ⬜ Not Started | ⬜ In Progress | ⬜ Completed | ⬜ Failed

**Notes:**
_________________________________________________
_________________________________________________
_________________________________________________

