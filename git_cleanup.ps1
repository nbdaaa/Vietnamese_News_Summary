# reset_repo.ps1
# This is an executable PowerShell script that will reset your Git repository

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "  Repository Reset Script" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "WARNING: This script will completely reset your Git repository!" -ForegroundColor Red
Write-Host "All previous history will be PERMANENTLY LOST." -ForegroundColor Red
Write-Host ""
Write-Host "This is the most reliable way to fix issues with large files." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to cancel now, or press Enter to continue..." -ForegroundColor White
Read-Host

# Create backup directory
$backupDir = "backup_data_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "Creating backup directory: $backupDir" -ForegroundColor Green
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

# Backup important data files
Write-Host "Backing up data files..." -ForegroundColor Yellow
$largeFile1 = "data/crawl_data/news_summaries (vietnamnet).csv"
$largeFile2 = "data/output/all_news_summaries.csv"

if (Test-Path $largeFile1) {
    $dir = Split-Path -Path $largeFile1 -Parent
    if (-not (Test-Path "$backupDir/$dir")) {
        New-Item -ItemType Directory -Path "$backupDir/$dir" -Force | Out-Null
    }
    Copy-Item -Path $largeFile1 -Destination "$backupDir/$largeFile1" -Force
    Write-Host "Backed up: $largeFile1" -ForegroundColor Green
}

if (Test-Path $largeFile2) {
    $dir = Split-Path -Path $largeFile2 -Parent
    if (-not (Test-Path "$backupDir/$dir")) {
        New-Item -ItemType Directory -Path "$backupDir/$dir" -Force | Out-Null
    }
    Copy-Item -Path $largeFile2 -Destination "$backupDir/$largeFile2" -Force
    Write-Host "Backed up: $largeFile2" -ForegroundColor Green
}

# Create a .gitignore file to prevent future issues
Write-Host "Creating .gitignore file..." -ForegroundColor Green
@"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Project specific - Ignore all large data files
data/output/
data/crawl_data/
*.csv

# OS specific
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo

# Logs
logs/
*.log
"@ | Out-File -FilePath .gitignore -Encoding utf8

# Remove large files
Write-Host "Removing large files..." -ForegroundColor Yellow
if (Test-Path $largeFile1) { Remove-Item -Path $largeFile1 -Force }
if (Test-Path $largeFile2) { Remove-Item -Path $largeFile2 -Force }

# Get current remote URL
$remoteUrl = git config --get remote.origin.url
Write-Host "Current remote URL: $remoteUrl" -ForegroundColor Cyan

# Delete .git directory to remove all history
Write-Host "Removing Git history by deleting .git directory..." -ForegroundColor Yellow
if (Test-Path ".git") { Remove-Item -Path ".git" -Recurse -Force }

# Initialize new Git repository
Write-Host "Initializing new Git repository..." -ForegroundColor Green
git init
git add .
git commit -m "Initial commit with clean repository"

# Add the remote origin back
git remote add origin $remoteUrl

Write-Host ""
Write-Host "Repository has been reset and all large files removed!" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. If you want to push to the same GitHub repository, you'll need to force push:" -ForegroundColor White
Write-Host "   git push -f origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. If you prefer to create a new GitHub repository instead, go to GitHub and:" -ForegroundColor White
Write-Host "   a. Create a new repository" -ForegroundColor White
Write-Host "   b. Update your local remote URL with: git remote set-url origin NEW_URL" -ForegroundColor White
Write-Host "   c. Push with: git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "Your backed up data files are in the '$backupDir' directory" -ForegroundColor Green
Write-Host ""