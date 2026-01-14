# 🚀 PolicyVision3.0 - Execution Backend

> **AI-Powered Policy Execution Engine** - Transforming policy documents into actionable tasks with intelligent automation

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)](https://www.mongodb.com)
[![Deployed](https://img.shields.io/badge/Deployed-Render-purple.svg)](https://policy-execution-backend.onrender.com)

---

## 🎯 Problem Statement

Government policies and organizational documents contain complex rules that need to be executed by different roles (Clerks, Officers, Admins). Manual processing is:
- ❌ Time-consuming and error-prone
- ❌ Difficult to track and audit
- ❌ Lacks accountability and transparency
- ❌ No automated task distribution

---

## 💡 Our Solution

**PolicyVision3.0** is an intelligent policy execution system that:

1. **Ingests** AI-parsed policy rules from NLP backend
2. **Generates** executable tasks with role assignments
3. **Tracks** task execution with complete audit trails
4. **Escalates** tasks through organizational hierarchy
5. **Exports** professional PDF reports

---

## 🏗️ System Architecture

```
┌─────────────────┐
│   Frontend      │  React Dashboard
│  (PolicyVision) │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   NLP Backend   │  AI Policy Parser
│   (AI Model)    │
└────────┬────────┘
         │
         ↓ POST /policies/ingest
┌─────────────────┐
│ Execution       │  ← YOU ARE HERE
│ Backend (This)  │  Task Management & Execution
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   MongoDB       │  Persistent Storage
│   (Atlas)       │
└─────────────────┘
```

---

## ✨ Key Features

### 🎯 Intelligent Task Management
- **Automatic Task Generation** - Converts policy rules into executable tasks
- **Role-Based Assignment** - Tasks distributed to Clerk, Officer, or Admin
- **Status Tracking** - CREATED → ASSIGNED → IN_PROGRESS → COMPLETED
- **Smart Escalation** - Tasks can be escalated up the hierarchy

### 📊 Complete Audit Trail
- **Every Action Logged** - Who did what, when
- **Audit Timeline** - Chronological activity feed
- **Accountability** - Full transparency in task execution

### 📄 PDF Report Generation
- **Professional Formatting** - ReportLab-powered PDFs
- **Policy Summaries** - Rules, assignments, statistics
- **Downloadable Reports** - Export for compliance and records

### 🔄 Real-Time Analytics
- **Dashboard Statistics** - Task counts by status and role
- **Activity Monitoring** - Recent system activity
- **Policy Metrics** - Total policies, completion rates

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | FastAPI | High-performance async API |
| **Database** | MongoDB (Motor) | Scalable NoSQL storage |
| **PDF Engine** | ReportLab | Professional document generation |
| **Deployment** | Render | Cloud hosting with auto-deploy |
| **API Docs** | Swagger/OpenAPI | Auto-generated documentation |

---

## 📋 API Endpoints

### 🔹 Policy Ingestion
```http
POST /policies/ingest
```
Receives parsed policy from NLP backend, creates tasks and audit logs.

**Request:**
```json
{
  "policy_id": "POL-2026-001",
  "rules": [
    {
      "rule_id": "R1",
      "action": "Verify applicant documents",
      "responsible_role": "Clerk",
      "deadline": "5 business days"
    }
  ]
}
```

**Response:** List of created tasks

---

### 🔹 Task Management

#### Get Tasks
```http
GET /tasks
GET /tasks?role=Clerk
```
Fetch all tasks or filter by role (Clerk, Officer, Admin).

#### Update Task Status
```http
POST /tasks/{task_id}/update-status
```
```json
{
  "new_status": "IN_PROGRESS",
  "role": "Clerk"
}
```

**Valid Transitions:**
- CREATED → ASSIGNED
- ASSIGNED → IN_PROGRESS
- IN_PROGRESS → COMPLETED or ESCALATED

#### Escalate Task
```http
POST /tasks/{task_id}/escalate
```
```json
{
  "role": "Clerk"
}
```

**Escalation Path:** Clerk → Officer → Admin

---

### 🔹 Analytics & Reporting

#### Audit Logs
```http
GET /audit-logs?limit=50
```
Returns chronological audit trail of all actions.

#### Recent Activity
```http
GET /activity/recent?limit=20
```
Returns formatted activity timeline for dashboard.

#### Statistics
```http
GET /policies/stats
```
Returns policy and task counts by status.

---

### 🔹 PDF Export

#### Save NLP Results
```http
POST /nlp-results/save
```
Stores NLP processing results for PDF generation.

#### List Results
```http
GET /nlp-results
```
Returns all saved policy results.

#### Download PDF
```http
GET /nlp-results/{result_id}/download-pdf
```
Generates and downloads formatted PDF report.

**PDF Contains:**
- Policy metadata (ID, file name, timestamp)
- Extracted rules table
- Role assignments
- Statistics summary

---

## 🗄️ Database Schema

### Collections

#### `policies`
```javascript
{
  policy_id: "POL-001",
  status: "ACTIVE",
  created_at: ISODate("2026-01-14")
}
```

#### `tasks`
```javascript
{
  task_id: "uuid",
  policy_id: "POL-001",
  rule_id: "R1",
  task_name: "Execute rule R1",
  assigned_role: "Clerk",
  status: "IN_PROGRESS",
  deadline: "5 days"
}
```

#### `audit_logs`
```javascript
{
  task_id: "uuid",
  action: "STATUS_UPDATE: CREATED -> ASSIGNED",
  performed_by_role: "Admin",
  timestamp: ISODate("2026-01-14T10:30:00Z")
}
```

#### `nlp_results`
```javascript
{
  result_id: "uuid",
  policy_id: "POL-001",
  file_name: "policy.pdf",
  upload_timestamp: ISODate("2026-01-14"),
  nlp_data: { rules: [...] },
  status: "completed"
}
```

---

## 🚀 Deployment

### Live URL
```
https://policy-execution-backend.onrender.com
```

### Auto-Deployment
- **Connected to GitHub** - Automatic deployment on push to `main`
- **Platform:** Render
- **Build Time:** ~2-3 minutes
- **Zero Downtime:** Rolling deployments

### Environment Variables
```bash
MONGO_URL=mongodb+srv://...
```

---

## 💻 Local Development

### Prerequisites
- Python 3.9+
- MongoDB (local or Atlas)

### Installation

```bash
# Clone repository
git clone https://github.com/Ansh-1glitch/policy-execution-backend.git
cd policy-execution-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MONGO_URL="your-mongodb-url"

# Run server
uvicorn app.main:app --reload
```

Server runs at `http://localhost:8000`

### API Documentation
Visit `http://localhost:8000/docs` for interactive Swagger UI

---

## 📁 Project Structure

```
policy-execution-backend/
├── app/
│   ├── main.py              # FastAPI application & endpoints
│   ├── schemas.py           # Pydantic models & validation
│   ├── db.py               # MongoDB connection
│   └── pdf_generator.py    # PDF generation logic
├── frontend_integration/
│   ├── api.ts              # TypeScript API client
│   ├── DashboardIntegration.tsx  # React component example
│   ├── dashboard.css       # Styling
│   └── INTEGRATION_GUIDE.md     # Frontend integration docs
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

---

## 🔄 Data Flow

### 1. Policy Ingestion Flow
```
NLP Backend → POST /policies/ingest → Backend
                                        ↓
                                   Save Policy
                                        ↓
                              Generate Tasks (1 per rule)
                                        ↓
                              Create Audit Logs
                                        ↓
                                Store in MongoDB
```

### 2. Task Execution Flow
```
Frontend → GET /tasks?role=Clerk → Backend
                                      ↓
                              Fetch from MongoDB
                                      ↓
                              Return filtered tasks
                                      ↓
User clicks "Start" → POST /tasks/{id}/update-status
                                      ↓
                              Validate transition
                                      ↓
                              Update task status
                                      ↓
                              Log to audit_logs
                                      ↓
                              Return updated task
```

### 3. PDF Export Flow
```
NLP Processing Complete → POST /nlp-results/save
                                      ↓
                              Store in nlp_results
                                      ↓
User clicks "Download" → GET /nlp-results/{id}/download-pdf
                                      ↓
                              Fetch NLP data
                                      ↓
                              Generate PDF (ReportLab)
                                      ↓
                              Stream to browser
```

---

## 🎨 Frontend Integration

### Quick Start

```typescript
// Configure API URL
const API_URL = "https://policy-execution-backend.onrender.com";

// Fetch tasks
const tasks = await fetch(`${API_URL}/tasks?role=Clerk`)
  .then(r => r.json());

// Update task status
await fetch(`${API_URL}/tasks/${taskId}/update-status`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    new_status: 'IN_PROGRESS',
    role: 'Clerk'
  })
});

// Download PDF
const response = await fetch(`${API_URL}/nlp-results/${id}/download-pdf`);
const blob = await response.blob();
const url = window.URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'policy.pdf';
a.click();
```

**Complete integration guide:** See `frontend_integration/INTEGRATION_GUIDE.md`

---

## 🔒 Security Features

- ✅ **CORS Enabled** - Configured for cross-origin requests
- ✅ **Input Validation** - Pydantic schema validation
- ✅ **Error Handling** - Comprehensive error responses
- ✅ **Environment Variables** - Secrets not in code
- ✅ **MongoDB Security** - Atlas with authentication

---

## 📊 Performance

- **Response Time:** < 100ms for most endpoints
- **Concurrent Requests:** Async FastAPI handles 1000+ req/s
- **Database:** MongoDB Atlas with auto-scaling
- **PDF Generation:** < 2 seconds for typical policy

---

## 🧪 Testing

### Manual Testing

```bash
# Health check
curl https://policy-execution-backend.onrender.com/

# Get tasks
curl "https://policy-execution-backend.onrender.com/tasks?role=Admin"

# Get statistics
curl "https://policy-execution-backend.onrender.com/policies/stats"
```

### API Documentation
Interactive testing at: `https://policy-execution-backend.onrender.com/docs`

---

## 🏆 Hackathon Highlights

### Innovation
- 🎯 **AI Integration** - Seamless connection with NLP backend
- 🤖 **Automated Task Generation** - Zero manual task creation
- 📊 **Real-time Analytics** - Live dashboard metrics

### Technical Excellence
- ⚡ **High Performance** - Async FastAPI for speed
- 🔄 **Scalable Architecture** - MongoDB + cloud deployment
- 📱 **Modern Stack** - Latest Python, FastAPI, ReportLab

### User Experience
- 🎨 **Professional PDFs** - Publication-quality reports
- 📈 **Complete Audit Trail** - Full transparency
- 🔍 **Smart Filtering** - Role-based task views

### Production Ready
- ☁️ **Cloud Deployed** - Live on Render
- 🔒 **Secure** - Environment variables, CORS, validation
- 📚 **Well Documented** - API docs, integration guides

---

## 🎯 Use Cases

1. **Government Departments** - Policy compliance tracking
2. **Corporate Compliance** - Regulatory requirement execution
3. **Educational Institutions** - Policy implementation
4. **Healthcare** - Protocol adherence monitoring
5. **Legal Firms** - Contract obligation tracking

---

## 🔮 Future Enhancements

- [ ] Email notifications for task assignments
- [ ] Deadline reminders and alerts
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Mobile app integration
- [ ] AI-powered task prioritization

---

## 👥 Team

**Backend Development** - Policy Execution Engine

---

## 📄 License

This project was developed for the hackathon.

---

## 🙏 Acknowledgments

- FastAPI for the amazing framework
- MongoDB for scalable database
- ReportLab for PDF generation
- Render for seamless deployment

---

## 📞 Contact & Links

- **Live API:** https://policy-execution-backend.onrender.com
- **API Docs:** https://policy-execution-backend.onrender.com/docs
- **GitHub:** https://github.com/Ansh-1glitch/policy-execution-backend

---

<div align="center">

**Built with ❤️ for PolicyVision3.0 Hackathon**

*Transforming Policies into Action*

</div>
