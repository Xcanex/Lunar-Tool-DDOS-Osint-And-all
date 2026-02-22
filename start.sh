#!/data/data/com.termux/files/usr/bin/bash
# Lunar Tool v3.5 - Termux Baslatici

clear

# --- Python kontrol ---
if ! command -v python &> /dev/null; then
    echo ""
    echo "  [!] Python bulunamadi!"
    echo "  [!] Once setup.sh calistirin: bash setup.sh"
    echo ""
    exit 1
fi

# --- Kutuphane kontrol ---
python -c "import rich; import requests; import phonenumbers; import whois; import dns; import faker" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo ""
    echo "  [!] Gerekli kutuphaneler eksik!"
    echo "  [!] Once setup.sh calistirin: bash setup.sh"
    echo ""
    exit 1
fi

# --- Basla ---
cd "$(dirname "$0")"
python main.py
