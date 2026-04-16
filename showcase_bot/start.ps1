<#
.SYNOPSIS
    Script for quick launch of Telegram Showcase Bot on Windows.
.DESCRIPTION
    This script checks for venv, creates it if necessary, installs deps and runs the bot.
#>

$ScriptPath = $MyInvocation.MyCommand.Path
$BotDirectory = Split-Path -Parent $ScriptPath
Set-Location $BotDirectory

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Bot Launch Sequence" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

if (-not (Test-Path ".env")) {
    Write-Host "Warning: .env not found! Copying from .env.example..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "Created .env. Please edit it and put your BOT_TOKEN." -ForegroundColor Green
        Pause
        exit
    } else {
        Write-Host "Error: .env.example not found!" -ForegroundColor Red
        Pause
        exit
    }
} else {
    $envContent = Get-Content ".env" | Out-String
    if ($envContent -match "YOUR_TELEGRAM_BOT_TOKEN_HERE") {
        Write-Host "Error: Real BOT_TOKEN not set in .env file." -ForegroundColor Red
        Pause
        exit
    }
}

if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error creating virtual environment!" -ForegroundColor Red
        Pause
        exit
    }
}

Write-Host "Activating virtual environment..." -ForegroundColor Cyan
$currentPolicy = Get-ExecutionPolicy
if ($currentPolicy -eq "Restricted") {
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
}

. ".\venv\Scripts\Activate.ps1"

Write-Host "Installing dependencies..." -ForegroundColor Cyan
$env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY="1"
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed successfully." -ForegroundColor Green
} else {
    Write-Host "Warning: Some dependencies might not have installed." -ForegroundColor Yellow
}

Write-Host "Starting bot..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host "-----------------------------------------" -ForegroundColor Cyan

python bot.py

Write-Host "-----------------------------------------" -ForegroundColor Cyan
Write-Host "Bot stopped." -ForegroundColor Yellow
Pause