@echo off
chcp 65001 >nul 2>&1
title Lunar Tool v3.5 - 115 Modules
color 0D

:: --- Python kontrol ---
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [!] Python bulunamadi! Once setup.bat calistirin.
    echo.
    pause
    exit /b 1
)

:: --- Kutuphaneleri kontrol ---
python -c "import rich; import requests; import psutil; import PIL; import qrcode; import phonenumbers; import whois; import dns; import faker" >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [!] Gerekli kutuphaneler eksik!
    echo  [!] Once setup.bat calistirin.
    echo.
    pause
    exit /b 1
)

:: --- Lunar Tool'u baslat ---
cd /d "%~dp0"
python main.py
if errorlevel 1 (
    echo.
    echo  [!] Bir hata olustu.
    echo.
    pause
)