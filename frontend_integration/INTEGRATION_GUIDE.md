# Frontend Integration Guide

## 🎯 Quick Start

This guide shows you how to integrate your ROCKET frontend with the backend API.

---

## 📁 Files Provided

All integration files are in the `frontend_integration/` folder:

| File | Purpose |
|------|---------|
| `api.ts` | Backend API functions |
| `DashboardIntegration.tsx` | React component example |
| `dashboard.css` | Styles for the dashboard |
| `INTEGRATION_GUIDE.md` | This file |

---

## 🚀 Step-by-Step Integration

### Step 1: Copy API Layer

Copy `api.ts` to your ROCKET project:

```bash
# From Hackathon folder
Copy-Item frontend_integration/api.ts -Destination C:\Users\kambo\Desktop\ROCKET\src\api\
```

Or manually copy the file to your ROCKET project's API folder (e.g., `src/api/` or `src/services/`).

---

### Step 2: Update Your Dashboard Component

Open your existing `DashboardInteractive.tsx` (or similar) and update it to use the API:

**Before (Mock Data):**
```typescript
const [tasks, setTasks] = useState([
  { task_id: "1", task_name: "Mock Task", status: "CREATED", ... }
]);
```

**After (Real API):**
```typescript
import { fetchTasks, updateTaskStatus, Task } from '../api/api';

const [tasks, setTasks] = useState<Task[]>([]);
const [isLoading, setIsLoading] = useState(true);

useEffect(() => {
  loadTasks();
}, []);

async function loadTasks() {
  try {
    setIsLoading(true);
    const data = await fetchTasks(selectedRole);
    setTasks(data);
  } catch (err) {
    console.error(err);
  } finally {
    setIsLoading(false);
  }
}
```

**See `DashboardIntegration.tsx` for a complete example.**

---

### Step 3: Add Styles

Copy `dashboard.css` to your ROCKET project:

```bash
Copy-Item frontend_integration/dashboard.css -Destination C:\Users\kambo\Desktop\ROCKET\src\styles\
```

Then import it in your component:
```typescript
import './styles/dashboard.css';
```

---

### Step 4: Update Backend URL (Optional)

If testing locally, update the backend URL in `api.ts`:

```typescript
// For production (default)
const BACKEND_URL = "https://policy-execution-backend.onrender.com";

// For local development
// const BACKEND_URL = "http://localhost:8000";
```

---

## 🔧 Backend Configuration

The backend has been updated with CORS support. No additional backend changes needed!

**What was added:**
- CORS middleware in `app/main.py`
- Allows all origins (for development)
- In production, restrict to your frontend URL

---

## 📊 Available API Functions

### 1. Fetch Tasks
```typescript
import { fetchTasks } from './api';

// Get all tasks (Admin view)
const allTasks = await fetchTasks();

// Get tasks for specific role
const clerkTasks = await fetchTasks('Clerk');
const officerTasks = await fetchTasks('Officer');
```

### 2. Update Task Status
```typescript
import { updateTaskStatus } from './api';

// Update task status
await updateTaskStatus(
  'task-id-123',
  'IN_PROGRESS',
  'Clerk'
);
```

### 3. Escalate Task
```typescript
import { escalateTask } from './api';

// Escalate task to next level
await escalateTask('task-id-123', 'Clerk');
```

### 4. Get Statistics
```typescript
import { getTaskStatistics } from './api';

// Get statistics for dashboard
const stats = await getTaskStatistics('Clerk');
console.log(stats.total, stats.completed, etc.);
```

### 5. Health Check
```typescript
import { checkBackendHealth } from './api';

// Check if backend is running
const health = await checkBackendHealth();
console.log(health.status); // "ok"
```

---

## 🎨 Component Structure

Your dashboard should have these key parts:

### 1. State Management
```typescript
const [tasks, setTasks] = useState<Task[]>([]);
const [isLoading, setIsLoading] = useState(true);
const [error, setError] = useState<string | null>(null);
const [selectedRole, setSelectedRole] = useState('Admin');
```

### 2. Data Loading
```typescript
useEffect(() => {
  loadTasks();
}, [selectedRole]);

async function loadTasks() {
  // See DashboardIntegration.tsx for full example
}
```

### 3. Task Actions
```typescript
async function handleUpdateStatus(taskId, newStatus) {
  await updateTaskStatus(taskId, newStatus, currentUserRole);
  await loadTasks(); // Refresh
}
```

### 4. UI Rendering
- Loading state: Show spinner
- Error state: Show error message with retry button
- Success state: Show tasks grid

---

## 🧪 Testing the Integration

### 1. Start Backend (if testing locally)
```bash
cd C:\Users\kambo\Desktop\Hackathon
uvicorn app.main:app --reload
```

### 2. Start Frontend
```bash
cd C:\Users\kambo\Desktop\ROCKET
npm run dev
# or
npm start
```

### 3. Test Checklist

- [ ] Dashboard loads without errors
- [ ] Tasks appear from backend
- [ ] Can switch between roles (Clerk, Officer, Admin)
- [ ] Task counts are correct
- [ ] Can click "Assign" on CREATED tasks
- [ ] Can click "Start" on ASSIGNED tasks
- [ ] Can click "Complete" on IN_PROGRESS tasks
- [ ] Can click "Escalate" on tasks
- [ ] Statistics update correctly
- [ ] Refresh button works
- [ ] Error handling works (try stopping backend)

---

## 🐛 Troubleshooting

### Issue: CORS Error
**Error:** `Access to fetch at '...' from origin '...' has been blocked by CORS policy`

**Solution:** Backend CORS is already configured. If still seeing this:
1. Ensure backend is running
2. Check backend URL in `api.ts` is correct
3. Restart both frontend and backend

---

### Issue: Tasks Not Loading
**Error:** `Failed to fetch tasks`

**Solution:**
1. Check backend is running: `curl https://policy-execution-backend.onrender.com/`
2. Check browser console for errors
3. Verify API URL in `api.ts`

---

### Issue: Status Update Fails
**Error:** `Invalid transition from X to Y`

**Solution:** Backend enforces valid state transitions:
- CREATED → ASSIGNED only
- ASSIGNED → IN_PROGRESS only
- IN_PROGRESS → COMPLETED or ESCALATED only

---

### Issue: No Tasks Appear
**Possible Causes:**
1. No tasks in database → Use NLP to ingest a policy first
2. Wrong role selected → Try "Admin" to see all tasks
3. Backend not running → Check backend URL

---

## 📋 State Transitions

Valid task status transitions:

```
CREATED
   ↓
ASSIGNED
   ↓
IN_PROGRESS
   ↓
COMPLETED or ESCALATED
```

**Escalation Path:**
- Clerk → Officer
- Officer → Admin

---

## 🎯 Quick Reference

| Action | API Function | Parameters |
|--------|-------------|------------|
| Load tasks | `fetchTasks(role?)` | Optional role filter |
| Update status | `updateTaskStatus(id, status, role)` | Task ID, new status, user role |
| Escalate | `escalateTask(id, role)` | Task ID, user role |
| Get stats | `getTaskStatistics(role?)` | Optional role filter |
| Health check | `checkBackendHealth()` | None |

---

## 🔗 Backend Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/tasks?role={role}` | GET | Fetch tasks |
| `/tasks/{id}/update-status` | POST | Update status |
| `/tasks/{id}/escalate` | POST | Escalate task |
| `/` | GET | Health check |

**Base URL:** `https://policy-execution-backend.onrender.com`

---

## ✅ Integration Checklist

- [ ] Copied `api.ts` to ROCKET project
- [ ] Updated dashboard component to use API
- [ ] Added loading and error states
- [ ] Copied CSS styles
- [ ] Tested task loading
- [ ] Tested task updates
- [ ] Tested role filtering
- [ ] Tested escalation
- [ ] Verified statistics display
- [ ] Tested error handling

---

## 🎉 You're Done!

Your frontend is now connected to the backend. All task data is real and updates are persisted to the database.

**Next Steps:**
1. Test thoroughly with different roles
2. Customize styles to match your design
3. Add more features as needed
4. Deploy frontend to production

---

## 📞 Need Help?

Check these files for examples:
- `DashboardIntegration.tsx` - Complete React component
- `api.ts` - All API functions with documentation
- `dashboard.css` - Styling examples

**Backend Documentation:**
- `PIPELINING_NLP_BACKEND.md` - API documentation
- `NLP_INTEGRATION_GUIDE.md` - NLP integration guide
