# PowerShell Script to Organize Backend into Main Hackathon Repository
# Run this script from Desktop

Write-Host "🚀 Organizing Backend for Hackathon Repository" -ForegroundColor Cyan
Write-Host "=" * 70

# Step 1: Clone main repository
Write-Host "`n[1/6] Cloning main repository..." -ForegroundColor Yellow
cd C:\Users\kambo\Desktop

if (Test-Path "ai-policy-execution-platform") {
    Write-Host "    Repository already exists, pulling latest changes..." -ForegroundColor Gray
    cd ai-policy-execution-platform
    git pull origin main
} else {
    git clone https://github.com/ankitsaini300000506-dotcom/ai-policy-execution-platform.git
    cd ai-policy-execution-platform
}

# Step 2: Create backend folder
Write-Host "`n[2/6] Creating backend folder..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "backend" | Out-Null
Write-Host "    ✓ backend/ folder created" -ForegroundColor Green

# Step 3: Copy backend files
Write-Host "`n[3/6] Copying backend files..." -ForegroundColor Yellow

# Copy app folder
Write-Host "    Copying app/..." -ForegroundColor Gray
Copy-Item -Path "..\Hackathon\app" -Destination "backend\app" -Recurse -Force

# Copy frontend_integration folder
Write-Host "    Copying frontend_integration/..." -ForegroundColor Gray
Copy-Item -Path "..\Hackathon\frontend_integration" -Destination "backend\frontend_integration" -Recurse -Force

# Copy individual files
Write-Host "    Copying requirements.txt..." -ForegroundColor Gray
Copy-Item -Path "..\Hackathon\requirements.txt" -Destination "backend\" -Force

Write-Host "    Copying .gitignore..." -ForegroundColor Gray
Copy-Item -Path "..\Hackathon\.gitignore" -Destination "backend\" -Force

Write-Host "    Copying README.md..." -ForegroundColor Gray
Copy-Item -Path "..\Hackathon\README.md" -Destination "backend\" -Force

Write-Host "    ✓ All files copied successfully" -ForegroundColor Green

# Step 4: Create main README if it doesn't exist
Write-Host "`n[4/6] Updating main README..." -ForegroundColor Yellow

$mainReadme = @"
# 🚀 AI Policy Execution Platform

> Complete end-to-end solution for automated policy execution using AI/NLP

[![Live Demo](https://img.shields.io/badge/Demo-Live-success)](https://policy-execution-backend.onrender.com)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-green)](https://fastapi.tiangolo.com)
[![Frontend](https://img.shields.io/badge/Frontend-React-blue)](https://reactjs.org)

---

## 🎯 Problem Statement

Government policies and organizational documents contain complex rules that need execution by different roles. Manual processing is time-consuming, error-prone, and lacks accountability.

---

## 💡 Our Solution

**AI Policy Execution Platform** - An intelligent system that:
1. **Parses** policy documents using AI/NLP
2. **Extracts** rules and assignments automatically
3. **Generates** executable tasks for different roles
4. **Tracks** execution with complete audit trails
5. **Exports** professional PDF reports

---

## 🏗️ Architecture

``````
┌─────────────┐
│  Frontend   │  React Dashboard
│  (Upload)   │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ NLP Backend │  AI Policy Parser
│ (AI Model)  │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Execution  │  Task Management
│   Backend   │  & Audit Trail
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   MongoDB   │  Data Storage
└─────────────┘
``````

---

## 📁 Project Structure

``````
ai-policy-execution-platform/
├── frontend/              # React dashboard
├── backend/              # FastAPI execution engine
│   ├── app/             # Core backend logic
│   ├── frontend_integration/  # Integration files
│   └── README.md        # Backend documentation
├── nlp/                 # AI model (if separate)
└── README.md           # This file
``````

---

## 🚀 Quick Start

### Backend
``````bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
``````

**Live Backend:** https://policy-execution-backend.onrender.com

### Frontend
``````bash
cd frontend
npm install
npm run dev
``````

---

## ✨ Key Features

### 🎯 Intelligent Task Management
- Automatic task generation from policy rules
- Role-based assignment (Clerk, Officer, Admin)
- Smart escalation through hierarchy

### 📊 Complete Audit Trail
- Every action logged
- Chronological timeline
- Full accountability

### 📄 PDF Report Generation
- Professional formatting
- Policy summaries
- Downloadable reports

### 🔄 Real-Time Analytics
- Dashboard statistics
- Activity monitoring
- Policy metrics

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React, TypeScript |
| Backend | FastAPI, Python |
| Database | MongoDB Atlas |
| AI/NLP | Custom AI Model |
| PDF | ReportLab |
| Deployment | Render |

---

## 📚 Documentation

- **Backend API:** See ``backend/README.md``
- **Frontend Integration:** See ``backend/frontend_integration/INTEGRATION_GUIDE.md``
- **API Docs:** https://policy-execution-backend.onrender.com/docs

---

## 🏆 Hackathon Highlights

### Innovation
- 🤖 AI-powered policy parsing
- 🎯 Automated task generation
- 📊 Real-time analytics

### Technical Excellence
- ⚡ High-performance async API
- 🔄 Scalable cloud architecture
- 📱 Modern tech stack

### User Experience
- 🎨 Professional PDF reports
- 📈 Complete audit trails
- 🔍 Smart role-based filtering

---

## 👥 Team

[Your Team Name]

---

## 📄 License

Developed for [Hackathon Name]

---

<div align="center">

**Built with ❤️ for Hackathon**

*Transforming Policies into Action*

</div>
"@

if (-not (Test-Path "README.md")) {
    $mainReadme | Out-File -FilePath "README.md" -Encoding UTF8
    Write-Host "    ✓ Main README.md created" -ForegroundColor Green
} else {
    Write-Host "    README.md already exists, skipping..." -ForegroundColor Gray
}

# Step 5: Git add and commit
Write-Host "`n[5/6] Committing changes..." -ForegroundColor Yellow
git add backend/
git add README.md

$commitMessage = "Add backend: FastAPI execution engine with task management, audit trails, and PDF export"
git commit -m $commitMessage

Write-Host "    ✓ Changes committed" -ForegroundColor Green

# Step 6: Push to GitHub
Write-Host "`n[6/6] Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host "`n" + "=" * 70
Write-Host "✅ SUCCESS! Backend organized and pushed to GitHub" -ForegroundColor Green
Write-Host "=" * 70

Write-Host "`n📋 Summary:" -ForegroundColor Cyan
Write-Host "   Repository: https://github.com/ankitsaini300000506-dotcom/ai-policy-execution-platform"
Write-Host "   Backend folder: backend/"
Write-Host "   Files copied: app/, frontend_integration/, requirements.txt, .gitignore, README.md"
Write-Host "   Live API: https://policy-execution-backend.onrender.com"

Write-Host "`n🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Visit your GitHub repository to verify"
Write-Host "   2. Check backend/README.md for complete documentation"
Write-Host "   3. Share repository link with judges!"

Write-Host "`n🏆 Your hackathon repository is ready!" -ForegroundColor Green
