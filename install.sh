#!/bin/bash

clear
echo "👻 GhostTool Installer"
echo "======================"

# Python kontrol
if ! command -v python3 &> /dev/null
then
    echo "[!] Python3 bulunamadı. Yükleniyor..."
    sudo apt update && sudo apt install python3 -y
fi

# Pip kontrol
if ! command -v pip3 &> /dev/null
then
    echo "[!] pip3 bulunamadı. Yükleniyor..."
    sudo apt install python3-pip -y
fi

# Paketleri yükle
echo "[+] Gerekli paketler yükleniyor..."
pip3 install -r requirements.txt

# İzinler
chmod +x ghost.py

echo ""
echo "✅ Kurulum tamamlandı!"
echo "Çalıştırmak için: python3 ghost.py"
