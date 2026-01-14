# Policy Execution Backend

Backend API for the PolicyVision3.0 system - handles policy ingestion, task management, and execution tracking.

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Locally

```bash
uvicorn app.main:app --reload
```

### Deploy to Render

Connected to GitHub - auto-deploys on push to `main` branch.

## 📋 API Endpoints

### Tasks
- `GET /tasks` - Get all tasks (optional `?role=` filter)
- `POST /tasks/{id}/update-status` - Update task status
- `POST /tasks/{id}/escalate` - Escalate task to higher role

### Policy Ingestion
- `POST /policies/ingest` - Ingest policy from NLP backend

### Analytics
- `GET /audit-logs` - Get audit trail
- `GET /activity/recent` - Get recent activity
- `GET /policies/stats` - Get statistics

### PDF Export
- `POST /nlp-results/save` - Save NLP results
- `GET /nlp-results` - List all results
- `GET /nlp-results/{id}/download-pdf` - Download PDF

## 🔗 Live URL

```
https://policy-execution-backend.onrender.com
```

## 📁 Project Structure

```
app/
├── main.py           # FastAPI application
├── schemas.py        # Pydantic models
├── db.py            # MongoDB connection
└── pdf_generator.py  # PDF generation

frontend_integration/
└── ...              # Frontend integration files
```

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** MongoDB (Motor)
- **PDF:** ReportLab
- **Deployment:** Render

## 📚 Documentation

See `frontend_integration/` folder for frontend integration guides.
