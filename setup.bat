@echo off
chcp 65001 >nul 2>&1
title Lunar Tool - Setup
color 0B

echo.
echo  ============================================
echo    LUNAR TOOL v3.5 - KURULUM
echo    115 Modules  ^|  12 Kategoriler
echo  ============================================
echo.

:: --- Python kontrol ---
echo  [*] Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [!] HATA: Python bulunamadi!
    echo  [!] Lutfen Python 3.10+ yukleyin:
    echo      https://www.python.org/downloads/
    echo.
    echo  [!] Kurulum sirasinda "Add Python to PATH" secenegini isaretleyin!
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo  [+] Python %PYVER% bulundu.
echo.

:: --- pip guncelle ---
echo  [*] pip guncelleniyor...
python -m pip install --upgrade pip >nul 2>&1
echo  [+] pip guncellendi.
echo.

:: --- Kutuphaneleri yukle ---
echo  [*] Kutuphaneler yukleniyor...
echo  ────────────────────────────────────────────
echo.

python -m pip install rich>=13.9.0
echo.
python -m pip install requests>=2.32.0
echo.
python -m pip install psutil>=6.1.0
echo.
python -m pip install Pillow>=11.1.0
echo.
python -m pip install qrcode>=7.4
echo.

echo    [*] OSINT gereksinimleri yukleniyor...
python -m pip install python-whois>=0.9.0
python -m pip install phonenumbers>=8.13.0
python -m pip install dnspython>=2.4.0
python -m pip install faker>=20.1.0
echo.

echo  ────────────────────────────────────────────
echo.

:: --- Kontrol ---
echo  [*] Kurulum dogrulaniyor...
python -c "import rich; import requests; import psutil; import PIL; import qrcode; import phonenumbers; import whois; import dns; import faker; print('  [+] Tum kutuphaneler basariyla yuklendi!')"
if errorlevel 1 (
    echo.
    echo  [!] Bazi kutuphaneler yuklenemedi.
    echo  [!] Manuel olarak deneyin: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo  ============================================
echo    KURULUM TAMAMLANDI!
echo    Baslatmak icin: start.bat
echo  ============================================
echo.
pause
