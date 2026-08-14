#!/bin/bash
# ==============================================================================
#  PARONI DOWNLOADER - Linux Auto-Installer & Systemd Service Creator
#  Supports: Ubuntu, Debian, Linux Mint, Fedora, Arch Linux, Manjaro, Pop!_OS
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}============================================================${NC}"
echo -e "${GREEN}       PARONI DOWNLOADER - LINUX INSTALLER (WEB SERVER)     ${NC}"
echo -e "${CYAN}============================================================${NC}"

if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[!] Por favor, execute este instalador como root (sudo ./install_linux.sh)${NC}"
  exit 1
fi

INSTALL_DIR="/opt/paroni-downloader"
SERVICE_PATH="/etc/systemd/system/paroni-downloader.service"
DESKTOP_PATH="/usr/share/applications/paroni-downloader.desktop"

echo -e "\n${CYAN}[1/4] Instalando dependências do sistema...${NC}"
if command -v apt &> /dev/null; then
    apt update && apt install -y python3 python3-pip python3-venv ffmpeg git
elif command -v dnf &> /dev/null; then
    dnf install -y python3 python3-pip ffmpeg git
elif command -v pacman &> /dev/null; then
    pacman -Sy --noconfirm python python-pip ffmpeg git
else
    echo -e "${YELLOW}[!] Gerenciador de pacotes não identificado. Certifique-se de ter python3, pip e ffmpeg instalados.${NC}"
fi

echo -e "\n${CYAN}[2/4] Copiando arquivos para ${INSTALL_DIR}...${NC}"
mkdir -p "$INSTALL_DIR"
cp -r downloader_core.py server.py config.json requirements.txt web temp "$INSTALL_DIR/" 2>/dev/null || true
mkdir -p "$INSTALL_DIR/temp"

echo -e "\n${CYAN}[3/4] Instalando pacotes Python em ambiente virtual...${NC}"
cd "$INSTALL_DIR"
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo -e "\n${CYAN}[4/4] Configurando Serviço Systemd e Atalho no Menu...${NC}"

# 1. Systemd Service creation
cat <<EOF > "$SERVICE_PATH"
[Unit]
Description=Paroni Downloader Web Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=${INSTALL_DIR}
ExecStart=${INSTALL_DIR}/venv/bin/python3 ${INSTALL_DIR}/server.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable paroni-downloader.service
systemctl restart paroni-downloader.service

# 2. Desktop Shortcut Creation
cat <<EOF > "$DESKTOP_PATH"
[Desktop Entry]
Version=1.0
Name=Paroni Downloader
Comment=Baixador Multimídia Web (YouTube, Spotify, TikTok, Instagram)
Exec=xdg-open http://localhost:3000
Icon=${INSTALL_DIR}/web/favIcon.ico
Terminal=false
Type=Application
Categories=Network;AudioVideo;
EOF

chmod +x "$DESKTOP_PATH"

echo -e "\n${GREEN}============================================================${NC}"
echo -e "${GREEN}  [✓] Instalação concluída com sucesso!${NC}"
echo -e "${GREEN}  [+] O servidor está rodando como serviço de sistema.${NC}"
echo -e "${CYAN}  [+] Acesse no navegador: http://localhost:3000${NC}"
echo -e "${CYAN}  [+] Status do serviço:  systemctl status paroni-downloader${NC}"
echo -e "${GREEN}============================================================${NC}\n"
