#!/bin/bash
# ==============================================================================
#  PARONI DOWNLOADER - Script Gerador de Pacote .DEB (Ubuntu / Debian / Mint)
# ==============================================================================

set -e

PACKAGE_NAME="paroni-downloader"
VERSION="2.5"
ARCH="all"
BUILD_DIR="build_deb"
DEB_FILE="${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"

echo "============================================================"
echo "   CRIANDO PACOTE DE INSTALAÇÃO .DEB PARA LINUX (DEBIAN/UBUNTU)"
echo "============================================================"

# Limpar builds antigos
rm -rf "$BUILD_DIR" "$DEB_FILE"

# Criar estrutura de diretórios do Debian
mkdir -p "$BUILD_DIR/DEBIAN"
mkdir -p "$BUILD_DIR/opt/paroni-downloader"
mkdir -p "$BUILD_DIR/usr/share/applications"

# Copiar arquivos do projeto
cp -r downloader_core.py server.py config.json requirements.txt web temp "$BUILD_DIR/opt/paroni-downloader/" 2>/dev/null || true
mkdir -p "$BUILD_DIR/opt/paroni-downloader/temp"

# Criar arquivo DEBIAN/control
cat <<EOF > "$BUILD_DIR/DEBIAN/control"
Package: ${PACKAGE_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Maintainer: Rafael Paroni <rafaelparoni.vercel.app>
Depends: python3, python3-pip, python3-venv, ffmpeg
Description: Baixador Multimidia Web (YouTube, Spotify, TikTok, Instagram)
 Servidor web responsivo e leve para download de videos e audios em alta qualidade.
EOF

# Criar script pós-instalação (postinst)
cat <<EOF > "$BUILD_DIR/DEBIAN/postinst"
#!/bin/sh
set -e

INSTALL_DIR="/opt/paroni-downloader"
SERVICE_PATH="/etc/systemd/system/paroni-downloader.service"

# Configurar ambiente virtual Python
if [ -d "\$INSTALL_DIR" ]; then
    cd "\$INSTALL_DIR"
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip >/dev/null 2>&1 || true
    ./venv/bin/pip install -r requirements.txt >/dev/null 2>&1 || true
fi

# Criar Serviço Systemd
cat <<SERVICE > "\$SERVICE_PATH"
[Unit]
Description=Paroni Downloader Web Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=\${INSTALL_DIR}
ExecStart=\${INSTALL_DIR}/venv/bin/python3 \${INSTALL_DIR}/server.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable paroni-downloader.service || true
systemctl restart paroni-downloader.service || true

exit 0
EOF
chmod 755 "$BUILD_DIR/DEBIAN/postinst"

# Criar script pré-remoção (prerm)
cat <<EOF > "$BUILD_DIR/DEBIAN/prerm"
#!/bin/sh
set -e

systemctl stop paroni-downloader.service 2>/dev/null || true
systemctl disable paroni-downloader.service 2>/dev/null || true
rm -f /etc/systemd/system/paroni-downloader.service
systemctl daemon-reload

exit 0
EOF
chmod 755 "$BUILD_DIR/DEBIAN/prerm"

# Criar atalho no menu de aplicativos do Linux (.desktop)
cat <<EOF > "$BUILD_DIR/usr/share/applications/paroni-downloader.desktop"
[Desktop Entry]
Version=1.0
Name=Paroni Downloader
Comment=Baixador Multimídia Web (YouTube, Spotify, TikTok, Instagram)
Exec=xdg-open http://localhost:3000
Icon=/opt/paroni-downloader/web/favIcon.ico
Terminal=false
Type=Application
Categories=Network;AudioVideo;
EOF

# Compilar pacote .deb
dpkg-deb --build "$BUILD_DIR" "$DEB_FILE"

# Limpar diretório temporário de build
rm -rf "$BUILD_DIR"

echo "============================================================"
echo " [✓] Pacote .DEB criado com sucesso: ${DEB_FILE}"
echo " [+] Para instalar no Ubuntu/Debian/Mint, execute:"
echo "     sudo dpkg -i ${DEB_FILE}"
echo "============================================================"
