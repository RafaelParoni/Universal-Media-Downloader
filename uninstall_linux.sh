#!/bin/bash
# ==============================================================================
#  PARONI DOWNLOADER - Linux Uninstaller Script
# ==============================================================================

set -e

if [ "$EUID" -ne 0 ]; then
  echo "[!] Execute como root (sudo ./uninstall_linux.sh)"
  exit 1
fi

echo "[1/3] Parando serviço systemd..."
systemctl stop paroni-downloader.service 2>/dev/null || true
systemctl disable paroni-downloader.service 2>/dev/null || true
rm -f /etc/systemd/system/paroni-downloader.service
systemctl daemon-reload

echo "[2/3] Removendo atalho de aplicativo..."
rm -f /usr/share/applications/paroni-downloader.desktop

echo "[3/3] Removendo arquivos de /opt/paroni-downloader..."
rm -rf /opt/paroni-downloader

echo "[✓] Paroni Downloader foi desinstalado do Linux com sucesso!"
