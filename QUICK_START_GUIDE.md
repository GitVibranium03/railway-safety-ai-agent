# 🚀 Quick Start Guide - Railway Safety Agent

## Step-by-Step Instructions

### **STEP 1: Install Dependencies** (One-time setup)

Open PowerShell and run:
```powershell
cd "C:\Users\vinay\Desktop\Train Accident Prevention"
pip install -r requirements.txt
```

---

### **STEP 2: Start the Backend Server**

**Option A: Using Batch File**
1. Open PowerShell
2. Navigate to project folder:
   ```powershell
   cd "C:\Users\vinay\Desktop\Train Accident Prevention"
   ```
3. Run:
   ```powershell
   .\start_backend.bat
   ```

**Option B: Direct Command**
```powershell
cd "C:\Users\vinay\Desktop\Train Accident Prevention"
uvicorn backend.main:app --reload --port 8000
```

**✅ Success Check:**
You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**⚠️ Keep this terminal window OPEN!** The backend must keep running.

---

### **STEP 3: Start the Frontend (Streamlit)**

**Open a NEW PowerShell window** (keep backend running in the first one):

1. Navigate to project folder:
   ```powershell
   cd "C:\Users\vinay\Desktop\Train Accident Prevention"
   ```
2. Run:
   ```powershell
   .\start_frontend.bat
   ```
   OR:
   ```powershell
   streamlit run frontend.py
   ```

**✅ Success Check:**
- Your browser should automatically open to `http://localhost:8501`
- You should see the Railway Safety Agent dashboard

---

### **STEP 4: Use the Application**

#### **Using the Streamlit Dashboard:**

1. **Set Visibility**: Use the slider (0-10,000 meters)
   - Example: Set to `500` meters

2. **Set Speed**: Use the slider (0-500 km/h)
   - Example: Set to `120` km/h

3. **Select Weather**: Choose from dropdown
   - Options: Clear, Rain, or Fog
   - Example: Select `Fog`

4. **Click "Assess Risk"** button

5. **View Results**:
   - **Risk Level**: Low / Medium / High (color-coded)
   - **Alert Message**: Safety alert
   - **Recommendation**: Actionable safety recommendations

#### **Test Different Scenarios:**

**Low Risk Example:**
- Visibility: `3000` m
- Speed: `80` km/h
- Weather: `Clear`

**Medium Risk Example:**
- Visibility: `800` m
- Speed: `120` km/h
- Weather: `Rain`

**High Risk Example:**
- Visibility: `200` m
- Speed: `150` km/h
- Weather: `Fog`

---

### **STEP 5: Test API Directly (Optional)**

**Open a NEW PowerShell window** (keep both backend and frontend running):

```powershell
# Test with curl (PowerShell)
curl -X POST http://localhost:8000/assess-risk `
  -H "Content-Type: application/json" `
  -d '{\"visibility\":800,\"speed\":130,\"weather\":\"Fog\"}'
```

**Or use Invoke-WebRequest (PowerShell native):**
```powershell
$body = @{
    visibility = 800
    speed = 130
    weather = "Fog"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/assess-risk" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

**Expected Response:**
```json
{
  "risk_level": "High",
  "alert_message": "🚨 EMERGENCY WARNING: HIGH RISK CONDITIONS",
  "recommendation": "HIGH RISK detected. IMMEDIATE ACTION REQUIRED: ..."
}
```

---

## 🔧 Troubleshooting

### **Problem: Backend won't start**

**Check 1: Port 8000 is already in use**
```powershell
netstat -ano | findstr :8000
```
If something is using port 8000, either:
- Stop that application, OR
- Change port in `start_backend.bat` to `--port 8001`

**Check 2: Python dependencies**
```powershell
pip install -r requirements.txt
```

**Check 3: Verify backend is running**
Open browser: `http://localhost:8000/health`
Should show: `{"status":"healthy","service":"railway-safety-agent"}`

---

### **Problem: Frontend can't connect to backend**

**Check 1: Backend is running**
- Look at backend terminal - should show "Uvicorn running"
- Test: `http://localhost:8000/health` in browser

**Check 2: Correct API URL**
- Frontend uses: `http://localhost:8000`
- If backend is on different port, edit `frontend.py` line 12:
  ```python
  API_URL = "http://localhost:8000"  # Change if needed
  ```

**Check 3: CORS is enabled**
- Already configured in `backend/main.py`
- Should work by default

---

### **Problem: "Module not found" errors**

**Solution:**
```powershell
cd "C:\Users\vinay\Desktop\Train Accident Prevention"
pip install -r requirements.txt
```

---

### **Problem: Streamlit opens but shows error**

**Check:**
1. Backend is running (Step 2)
2. Backend is accessible: `http://localhost:8000/health`
3. Check browser console (F12) for errors

---

## 📋 Quick Reference

### **Three Terminal Windows Needed:**

1. **Terminal 1 - Backend:**
   ```powershell
   cd "C:\Users\vinay\Desktop\Train Accident Prevention"
   uvicorn backend.main:app --reload --port 8000
   ```

2. **Terminal 2 - Frontend:**
   ```powershell
   cd "C:\Users\vinay\Desktop\Train Accident Prevention"
   streamlit run frontend.py
   ```

3. **Terminal 3 - Optional (for API testing):**
   ```powershell
   # Test API here
   ```

### **URLs:**
- **Backend API**: `http://localhost:8000`
- **Frontend Dashboard**: `http://localhost:8501`
- **API Health Check**: `http://localhost:8000/health`
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)

---

## ✅ Success Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Backend running (Terminal 1 shows "Uvicorn running")
- [ ] Frontend running (Browser opens to dashboard)
- [ ] Can see input sliders (Visibility, Speed, Weather)
- [ ] "Assess Risk" button works
- [ ] Risk assessment results display correctly
- [ ] API health check works (`http://localhost:8000/health`)

---

**Need Help?** Check the main `README.md` for more details!
