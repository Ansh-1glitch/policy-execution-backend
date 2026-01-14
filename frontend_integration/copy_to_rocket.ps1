#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Quick integration script to copy frontend files to ROCKET project

.DESCRIPTION
    This script copies the integration files from Hackathon to ROCKET frontend

.EXAMPLE
    .\copy_to_rocket.ps1
#>

$HackathonPath = "C:\Users\kambo\Desktop\Hackathon\frontend_integration"
$RocketPath = "C:\Users\kambo\Desktop\ROCKET"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Frontend Integration - File Copy Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if ROCKET folder exists
if (-not (Test-Path $RocketPath)) {
    Write-Host "ERROR: ROCKET folder not found at $RocketPath" -ForegroundColor Red
    Write-Host "Please verify the ROCKET frontend location." -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Found ROCKET frontend at: $RocketPath" -ForegroundColor Green
Write-Host ""

# Create destination folders if they don't exist
$ApiDest = Join-Path $RocketPath "src\api"
$StylesDest = Join-Path $RocketPath "src\styles"
$ComponentsDest = Join-Path $RocketPath "src\components"

Write-Host "Creating destination folders..." -ForegroundColor Cyan

if (-not (Test-Path $ApiDest)) {
    New-Item -ItemType Directory -Path $ApiDest -Force | Out-Null
    Write-Host "  Created: $ApiDest" -ForegroundColor Green
}

if (-not (Test-Path $StylesDest)) {
    New-Item -ItemType Directory -Path $StylesDest -Force | Out-Null
    Write-Host "  Created: $StylesDest" -ForegroundColor Green
}

if (-not (Test-Path $ComponentsDest)) {
    New-Item -ItemType Directory -Path $ComponentsDest -Force | Out-Null
    Write-Host "  Created: $ComponentsDest" -ForegroundColor Green
}

Write-Host ""

# Copy files
Write-Host "Copying integration files..." -ForegroundColor Cyan

# Copy API layer
$ApiSource = Join-Path $HackathonPath "api.ts"
if (Test-Path $ApiSource) {
    Copy-Item $ApiSource -Destination $ApiDest -Force
    Write-Host "  ✓ Copied api.ts to $ApiDest" -ForegroundColor Green
} else {
    Write-Host "  ✗ api.ts not found" -ForegroundColor Red
}

# Copy Dashboard component
$DashboardSource = Join-Path $HackathonPath "DashboardIntegration.tsx"
if (Test-Path $DashboardSource) {
    Copy-Item $DashboardSource -Destination $ComponentsDest -Force
    Write-Host "  ✓ Copied DashboardIntegration.tsx to $ComponentsDest" -ForegroundColor Green
} else {
    Write-Host "  ✗ DashboardIntegration.tsx not found" -ForegroundColor Red
}

# Copy CSS
$CssSource = Join-Path $HackathonPath "dashboard.css"
if (Test-Path $CssSource) {
    Copy-Item $CssSource -Destination $StylesDest -Force
    Write-Host "  ✓ Copied dashboard.css to $StylesDest" -ForegroundColor Green
} else {
    Write-Host "  ✗ dashboard.css not found" -ForegroundColor Red
}

# Copy integration guide
$GuideSource = Join-Path $HackathonPath "INTEGRATION_GUIDE.md"
if (Test-Path $GuideSource) {
    Copy-Item $GuideSource -Destination $RocketPath -Force
    Write-Host "  ✓ Copied INTEGRATION_GUIDE.md to $RocketPath" -ForegroundColor Green
} else {
    Write-Host "  ✗ INTEGRATION_GUIDE.md not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Integration files copied successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Open ROCKET project and review copied files" -ForegroundColor White
Write-Host "2. Update your existing dashboard component to use the API" -ForegroundColor White
Write-Host "3. Import the CSS in your component" -ForegroundColor White
Write-Host "4. Test the integration" -ForegroundColor White
Write-Host ""
Write-Host "See INTEGRATION_GUIDE.md for detailed instructions." -ForegroundColor Cyan
Write-Host ""
