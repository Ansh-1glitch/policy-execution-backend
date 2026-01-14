# NLP Backend URL Configuration

## 🔗 Current NLP Backend URL

```
https://eighty-clubs-stop.loca.lt
```

## 📋 Available Endpoints

### 1. POST /api/policy/process
**Purpose:** Process policy document and extract rules

**URL:** `https://eighty-clubs-stop.loca.lt/api/policy/process`

---

### 2. POST /api/policy/clarify
**Purpose:** Submit clarifications for ambiguous rules

**URL:** `https://eighty-clubs-stop.loca.lt/api/policy/clarify`

---

### 3. POST /api/policy/submit
**Purpose:** Submit processed policy to Execution Backend

**URL:** `https://eighty-clubs-stop.loca.lt/api/policy/submit`

**Note:** This endpoint syncs data to the Execution Backend at:
```
https://policy-execution-backend.onrender.com
```

---

## 🔄 Integration Flow

```
Frontend → NLP Backend → Execution Backend
          (loca.lt)      (onrender.com)
```

1. **Frontend** sends policy to NLP Backend
2. **NLP Backend** processes and extracts rules
3. **NLP Backend** forwards to Execution Backend via `/api/policy/submit`
4. **Execution Backend** creates tasks and stores in MongoDB

---

## ⚠️ Important Notes

### LocalTunnel URL
- **Type:** Temporary tunnel URL
- **Persistence:** URL changes when server restarts
- **Update Required:** Frontend must update URL when NLP server restarts

### For Production
Consider using:
- **ngrok** - More stable tunnels
- **Render/Railway** - Permanent deployment
- **Custom domain** - Best for production

---

## 📞 For Frontend Team

**Update your frontend API configuration to:**

```typescript
const NLP_BACKEND_URL = "https://eighty-clubs-stop.loca.lt";

// Process policy
await fetch(`${NLP_BACKEND_URL}/api/policy/process`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ policy_text: "..." })
});

// Submit clarifications
await fetch(`${NLP_BACKEND_URL}/api/policy/clarify`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    policy_id: "POL-001",
    rule_id: "R1",
    clarified_responsible_role: "Clerk",
    clarified_deadline: "5 days"
  })
});
```

---

## ✅ Status

- ✅ NLP Backend: Running at `https://eighty-clubs-stop.loca.lt`
- ✅ Execution Backend: Running at `https://policy-execution-backend.onrender.com`
- ✅ All endpoints verified and operational

---

**Last Updated:** 2026-01-14 12:24 IST
