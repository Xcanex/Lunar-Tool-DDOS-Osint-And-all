#!/data/data/com.termux/files/usr/bin/bash
# ══════════════════════════════════════════════════════════════
#  Lunar Tool v3.5 - Termux Kurulum
#  115 Modules  |  12 Kategoriler
# ══════════════════════════════════════════════════════════════

clear
echo ""
echo "  ============================================"
echo "    LUNAR TOOL v3.5 - TERMUX KURULUM"
echo "    115 Modules  |  12 Kategoriler"
echo "  ============================================"
echo ""

# --- Termux kontrol ---
if [ ! -d "/data/data/com.termux" ]; then
    echo "  [!] Bu script Termux icin tasarlanmistir."
    echo "  [!] Baska bir Linux dagitiminda calistiriyorsaniz"
    echo "  [!] paket yoneticinizi kullanin."
    echo ""
fi

# --- Sistem guncelle ---
echo "  [*] Sistem guncelleniyor..."
pkg update -y > /dev/null 2>&1
pkg upgrade -y > /dev/null 2>&1
echo "  [+] Sistem guncellendi."
echo ""

# --- Python yukle ---
echo "  [*] Python kontrol ediliyor..."
if ! command -v python &> /dev/null; then
    echo "  [*] Python yukleniyor..."
    pkg install python -y > /dev/null 2>&1
fi
PYVER=$(python --version 2>&1)
echo "  [+] $PYVER bulundu."
echo ""

# --- Gerekli sistem paketler ---
echo "  [*] Gerekli sistem paketleri yukleniyor..."
pkg install git -y > /dev/null 2>&1
pkg install libjpeg-turbo -y > /dev/null 2>&1
pkg install libpng -y > /dev/null 2>&1
pkg install freetype -y > /dev/null 2>&1
pkg install libxml2 -y > /dev/null 2>&1
pkg install libxslt -y > /dev/null 2>&1
pkg install build-essential -y > /dev/null 2>&1
echo "  [+] Sistem paketleri yuklendi."
echo ""

# --- pip guncelle ---
echo "  [*] pip guncelleniyor..."
pip install --upgrade pip > /dev/null 2>&1
echo "  [+] pip guncellendi."
echo ""

# --- Python kutuphaneleri ---
echo "  [*] Python kutuphaneleri yukleniyor..."
echo "  ────────────────────────────────────────────"
echo ""

echo "  [*] rich yukleniyor..."
pip install rich 2>&1 | tail -1
echo ""

echo "  [*] requests yukleniyor..."
pip install requests 2>&1 | tail -1
echo ""

echo "  [*] psutil yukleniyor..."
pip install psutil 2>&1 | tail -1
echo ""

echo "  [*] Pillow yukleniyor..."
pip install Pillow 2>&1 | tail -1
echo ""

echo "  [*] qrcode yukleniyor..."
pip install qrcode 2>&1 | tail -1
echo ""

echo "  [*] OSINT gereksinimleri yukleniyor..."
pip install python-whois phonenumbers dnspython faker 2>&1 | tail -1
echo ""

echo "  ────────────────────────────────────────────"
echo ""

# --- Dogrulama ---
echo "  [*] Kurulum dogrulaniyor..."
python -c "
import rich, requests, psutil, PIL, qrcode
print('  [+] Tum kutuphaneler basariyla yuklendi!')
" 2>&1

if [ $? -ne 0 ]; then
    echo ""
    echo "  [!] Bazi kutuphaneler yuklenemedi."
    echo "  [!] Manuel deneyin: pip install -r requirements.txt"
    echo ""
    exit 1
fi

# --- Calisma izni ---
chmod +x start.sh 2>/dev/null

echo ""
echo "  ============================================"
echo "    KURULUM TAMAMLANDI!"
echo "    Baslatmak icin: bash start.sh"
echo "    veya: python main.py"
echo "  ============================================"
echo ""
