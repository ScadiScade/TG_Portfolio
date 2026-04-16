<#
.SYNOPSIS
    Скрипт для быстрого запуска Telegram Showcase Bot на Windows.
.DESCRIPTION
    Этот скрипт проверяет наличие виртуального окружения (venv),
    создает его при необходимости, устанавливает зависимости и запускает бота.
#>

$ScriptPath = $MyInvocation.MyCommand.Path
$BotDirectory = Split-Path -Parent $ScriptPath
Set-Location $BotDirectory

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🤖 Запуск Telegram Showcase Bot" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Проверка файла .env
if (-not (Test-Path ".env")) {
    Write-Host "⚠️ Файл .env не найден! Создаю из .env.example..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Создан файл .env. Пожалуйста, откройте его и впишите свой BOT_TOKEN." -ForegroundColor Green
        Write-Host "Запуск отменен, так как нужно настроить токен." -ForegroundColor Red
        Pause
        exit
    } else {
        Write-Host "❌ Ошибка: Файл .env.example не найден!" -ForegroundColor Red
        Pause
        exit
    }
} else {
    # Проверка, не остался ли дефолтный токен
    $envContent = Get-Content ".env" | Out-String
    if ($envContent -match "YOUR_TELEGRAM_BOT_TOKEN_HERE") {
        Write-Host "❌ Ошибка: В файле .env не указан реальный BOT_TOKEN!" -ForegroundColor Red
        Write-Host "Пожалуйста, откройте файл .env и замените YOUR_TELEGRAM_BOT_TOKEN_HERE на токен от @BotFather." -ForegroundColor Yellow
        Pause
        exit
    }
}

# Настройка виртуального окружения
if (-not (Test-Path "venv")) {
    Write-Host "📦 Создание виртуального окружения Python (venv)..." -ForegroundColor Cyan
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Ошибка при создании виртуального окружения! Убедитесь, что Python установлен." -ForegroundColor Red
        Pause
        exit
    }
}

Write-Host "🔄 Активация виртуального окружения..." -ForegroundColor Cyan
# Обход политики выполнения скриптов (Execution Policy) только для этого процесса, если нужно
$currentPolicy = Get-ExecutionPolicy
if ($currentPolicy -eq "Restricted") {
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
}

. ".\venv\Scripts\Activate.ps1"

Write-Host "📥 Проверка и установка зависимостей из requirements.txt..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Все зависимости установлены." -ForegroundColor Green
} else {
    Write-Host "⚠️ Внимание: Возможно, не все зависимости установились." -ForegroundColor Yellow
}

Write-Host "🚀 Запуск бота..." -ForegroundColor Green
Write-Host "Для остановки бота нажмите Ctrl+C" -ForegroundColor Yellow
Write-Host "-----------------------------------------" -ForegroundColor Cyan

python bot.py

Write-Host "-----------------------------------------" -ForegroundColor Cyan
Write-Host "🛑 Бот остановлен." -ForegroundColor Yellow
Pause
