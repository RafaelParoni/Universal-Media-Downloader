# Paroni Downloader (v2.5 Web)

![Versão](https://img.shields.io/badge/versão-2.5_Web-blue.svg)
![Plataforma](https://img.shields.io/badge/plataforma-Windows_%7C_Linux-lightgrey.svg)
![Licença](https://img.shields.io/badge/licença-MIT-green.svg)

O **Paroni Downloader** é uma aplicação web moderna, responsiva e de alta performance projetada para baixar vídeos e áudios das principais redes sociais e plataformas de streaming (YouTube, Spotify, TikTok, Instagram, Twitter, Reddit, Pinterest, Twitch, Kwai, Vimeo, SoundCloud, Bandcamp, BiliBili, Facebook).

---

## ✨ Recursos do Projeto

- 🌐 **Servidor Web Headless (Porta 3000)**: Executa como servidor backend e permite acesso local (`http://localhost:3000`) ou em rede local via IP (`http://<IP_DA_REDE>:3000`).
- 🔒 **Modo Navegador & Autolimpeza (5 Minutos)**: Os downloads são processados temporariamente na pasta `temp/`, entregues diretamente para o seu navegador e **excluídos permanentemente do servidor após 5 minutos**.
- 🛡️ **Configuração MESTRE Protegida por PIN**: Painel administrativo protegido por senha PIN para alterar a porta do servidor, alternar modo de acesso (IP de rede vs Apenas Localhost) e controlar o processo do servidor (Reiniciar / Desligar).
- 💻 **Histórico & Preferências Isolados por Dispositivo**: O histórico de downloads, idioma e atalhos da barra lateral são salvos individualmente no `localStorage` de cada computador/navegador.
- 📱 **Interface 100% Responsiva & Mobile Navigation**: Layout adaptativo para Desktop e interface dedicada para Smartphones com atalhos no topo e barra de navegação inferior (Bottom Nav).

---

## 🚀 Como Executar pelo Código-Fonte

### Pré-requisitos
- Python 3.9 ou superior.
- Dependências instaladas (`yt-dlp`, `imageio_ffmpeg`).

### Passos:
1. Clone o repositório:
   ```bash
   git clone https://github.com/RafaelParoni/Paroni-Downloader.git
   cd Paroni-Downloader
   ```
2. Instale as dependências:
   ```bash
   py -m pip install -r requirements.txt
   ```
3. Inicie o servidor:
   ```bash
   py server.py
   ```
4. Acesse no navegador em `http://localhost:3000`.

---

## 🪟 Instalação no Windows (PyInstaller + Inno Setup)

Você pode compilar o projeto em um executável nativo do Windows e gerar um instalador de instalação rápida (`setup.exe`):

1. **Compilar Executável (`.exe`) com PyInstaller:**
   ```bash
   py -m PyInstaller --noconfirm paroni_downloader.spec
   ```
   *O executável autônomo será gerado na pasta `dist/ParoniDownloaderServer.exe`.*

2. **Gerar Instalador Windows (`Setup.exe`) com Inno Setup:**
   - Abra o aplicativo **Inno Setup Compiler**.
   - Abra o arquivo `installer_windows.iss`.
   - Clique em **Compile** (ou dê `Ctrl + F9`).
   - O instalador oficial `ParoniDownloader-Setup-v2.5.exe` será gerado na pasta `installer_output/`.

---

## 🐧 Instalação no Linux (Pacote .DEB & Script Auto-Installer)

Oferecemos duas formas nativas para instalar no Linux:

### Opção 1: Pacote de Instalação Gráfica `.DEB` (Ubuntu / Debian / Linux Mint / Pop!_OS)
1. Gere o pacote `.deb`:
   ```bash
   chmod +x create_deb_package.sh
   ./create_deb_package.sh
   ```
2. O arquivo **`paroni-downloader_2.5_all.deb`** será gerado.
3. Para instalar, basta dar **2 cliques no arquivo `.deb`** para abrir a Central de Programas do Ubuntu/Debian e clicar em **Instalar**, ou rodar:
   ```bash
   sudo dpkg -i paroni-downloader_2.5_all.deb
   ```

### Opção 2: Script Auto-Installer de Terminal (Qualquer Distro Linux)
1. Instalação com registro de serviço no `systemd` e atalho no menu:
   ```bash
   chmod +x install_linux.sh
   sudo ./install_linux.sh
   ```
2. Para verificar o status do servidor no Linux:
   ```bash
   sudo systemctl status paroni-downloader
   ```
3. Para desinstalar do Linux:
   ```bash
   chmod +x uninstall_linux.sh
   sudo ./uninstall_linux.sh
   ```

---

## 👤 Autor e Links

- **Autor**: Rafael Paroni
- **GitHub**: [https://github.com/RafaelParoni/Paroni-Downloader](https://github.com/RafaelParoni/Paroni-Downloader)
- **Site**: [https://rafaelparoni.vercel.app/](https://rafaelparoni.vercel.app/)

---
*Licença MIT - Uso pessoal e educacional.*
