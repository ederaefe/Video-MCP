<#
.SYNOPSIS
    Automates the weekly backup of VEDIT to https://github.com/ederaefe/Video-MCP

.DESCRIPTION
    1. Optionally commits pending changes in VEDIT with a timestamp.
    2. Pushes VEDIT main branch to backup:vedit.
    3. Synchronizes clean source files to ../mcp-video/vedit (excluding caches and dependencies).
    4. Commits and pushes the mcp-video main branch to origin.
#>

param(
    [switch]$AutoCommit,
    [string]$CommitMessage = "chore: weekly sync checkpoint from VEDIT"
)

$ErrorActionPreference = "Stop"
$VeditRoot = (Resolve-Path "$PSScriptRoot\..").Path
$McpVideoRoot = (Resolve-Path "$VeditRoot\..\mcp-video").Path
$Destination = Join-Path $McpVideoRoot "vedit"

Write-Host "[1/4] Checking VEDIT repository state..." -ForegroundColor Cyan
Set-Location $VeditRoot

$status = git status --porcelain
if ($status) {
    if ($AutoCommit) {
        Write-Host "Staging and committing pending VEDIT changes..." -ForegroundColor Yellow
        git add -A
        git commit -m $CommitMessage
    } else {
        Write-Host "Warning: VEDIT working tree has uncommitted changes. Run with -AutoCommit to commit automatically." -ForegroundColor Yellow
    }
}

Write-Host "[2/4] Pushing VEDIT history to backup mirror branch (vedit)..." -ForegroundColor Cyan
git push backup main:vedit

Write-Host "[3/4] Mirroring files to $Destination..." -ForegroundColor Cyan
if (-not (Test-Path $Destination)) {
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
}

$excludeDirs = @(".git", ".venv", "node_modules", "__pycache__", ".pytest_cache", ".hypothesis", "dist", "build", ".claude")
$excludeFiles = @("*.pyc", "*.pyo", "*.tmp", "*.log")

$robocopyArgs = @(
    $VeditRoot,
    $Destination,
    "/MIR",
    "/XD"
) + $excludeDirs + @("/XF") + $excludeFiles + @("/R:1", "/W:1", "/NJH", "/NJS", "/NDL")

# Robocopy exits with codes 0-7 on success
robocopy @robocopyArgs | Out-Null
if ($LASTEXITCODE -gt 7) {
    Write-Error "Robocopy failed with exit code $LASTEXITCODE"
}

Write-Host "[4/4] Committing and pushing to Video-MCP main branch..." -ForegroundColor Cyan
Set-Location $McpVideoRoot
git add vedit/
$mcpStatus = git status --porcelain vedit/
if ($mcpStatus) {
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    git commit -m "chore(vedit): sync backup from VEDIT ($timestamp)"
    git push origin main
    Write-Host "Backup synchronization successfully completed and pushed to Video-MCP." -ForegroundColor Green
} else {
    Write-Host "No file changes detected in vedit/; mirror branch is already up to date." -ForegroundColor Green
}

Set-Location $VeditRoot
