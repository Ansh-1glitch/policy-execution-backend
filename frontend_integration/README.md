# Frontend Integration - Quick Reference

## 📦 What's Included

All files are in `frontend_integration/` folder:

- **`api.ts`** - Backend API functions (TypeScript)
- **`DashboardIntegration.tsx`** - React component example
- **`dashboard.css`** - Modern dashboard styles
- **`INTEGRATION_GUIDE.md`** - Detailed step-by-step guide
- **`copy_to_rocket.ps1`** - Automated copy script
- **`README.md`** - This file

---

## 🚀 Quick Start (3 Steps)

### Option 1: Automated (Recommended)

```powershell
cd C:\Users\kambo\Desktop\Hackathon\frontend_integration
.\copy_to_rocket.ps1
```

This will automatically copy all files to your ROCKET project.

### Option 2: Manual

1. **Copy API Layer:**
   ```
   Copy api.ts → ROCKET/src/api/api.ts
   ```

2. **Copy Component Example:**
   ```
   Copy DashboardIntegration.tsx → ROCKET/src/components/
   ```

3. **Copy Styles:**
   ```
   Copy dashboard.css → ROCKET/src/styles/
   ```

---

## 🔧 Integration Steps

### 1. Update Your Dashboard Component

Replace mock data with real API calls:

```typescript
import { fetchTasks, updateTaskStatus } from '../api/api';

// In your component
useEffect(() => {
  async function loadTasks() {
    const tasks = await fetchTasks(selectedRole);
    setTasks(tasks);
  }
  loadTasks();
}, [selectedRole]);
```

### 2. Add Loading & Error States

```typescript
const [isLoading, setIsLoading] = useState(true);
const [error, setError] = useState(null);

if (isLoading) return <div>Loading...</div>;
if (error) return <div>Error: {error}</div>;
```

### 3. Handle Task Actions

```typescript
async function handleUpdateStatus(taskId, newStatus) {
  await updateTaskStatus(taskId, newStatus, currentUserRole);
  await loadTasks(); // Refresh
}
```

**See `DashboardIntegration.tsx` for complete example.**

---

## ✅ Backend Ready

Backend is already configured with:
- ✅ CORS enabled
- ✅ All endpoints working
- ✅ Deployed at: `https://policy-execution-backend.onrender.com`

No backend changes needed!

---

## 📋 Available API Functions

```typescript
// Fetch tasks
await fetchTasks('Clerk');

// Update status
await updateTaskStatus(taskId, 'IN_PROGRESS', 'Clerk');

// Escalate task
await escalateTask(taskId, 'Clerk');

// Get statistics
await getTaskStatistics('Clerk');

// Health check
await checkBackendHealth();
```

---

## 🧪 Testing

1. **Start your ROCKET frontend:**
   ```bash
   cd C:\Users\kambo\Desktop\ROCKET
   npm run dev
   ```

2. **Open browser and verify:**
   - Tasks load from backend
   - Can update task status
   - Statistics display correctly
   - Role filtering works

---

## 📚 Documentation

- **`INTEGRATION_GUIDE.md`** - Complete integration guide
- **`api.ts`** - API documentation in code comments
- **`DashboardIntegration.tsx`** - Component example with comments

---

## 🐛 Troubleshooting

**Tasks not loading?**
- Check backend URL in `api.ts`
- Verify backend is running
- Check browser console for errors

**CORS errors?**
- Backend CORS is already configured
- Restart both frontend and backend

**Status update fails?**
- Check valid state transitions in guide
- Verify role permissions

---

## 🎯 State Transitions

```
CREATED → ASSIGNED → IN_PROGRESS → COMPLETED/ESCALATED
```

---

## 📞 Need Help?

Read the **`INTEGRATION_GUIDE.md`** for detailed instructions, examples, and troubleshooting.

---

## ✨ You're Ready!

Your frontend can now:
- ✅ Fetch real tasks from backend
- ✅ Update task statuses
- ✅ Escalate tasks
- ✅ Display real-time statistics
- ✅ Filter by role
- ✅ Handle errors gracefully

**Happy coding! 🚀**
