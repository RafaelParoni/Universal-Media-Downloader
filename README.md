# Paroni Downloader (v2.5 Web)

![Version](https://img.shields.io/badge/version-2.5_Web-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows_%7C_Linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Paroni Downloader** is a modern, responsive web application and headless server designed to download video and audio from over 14 platforms (YouTube, Spotify, TikTok, Instagram, Twitter, Reddit, Pinterest, Twitch, Kwai, Vimeo, SoundCloud, Bandcamp, BiliBili, Facebook) directly in your browser!

---

## ✨ Features

- 🌐 **Headless Web Server (Port 3000)**: Runs as a backend server accessible via `http://localhost:3000` or via local network IP (`http://<LAN_IP>:3000`).
- 🔒 **Browser Downloads & 5-Minute Auto-Cleanup**: Files are processed temporarily in `temp/`, sent directly to your browser, and **permanently deleted from the server after 5 minutes**.
- 🛡️ **PIN-Protected MASTER Settings**: Password-protected master settings panel to change server port, toggle host bind mode (`0.0.0.0` vs `127.0.0.1`), and control server process (Restart / Stop).
- 💻 **Per-Device History & Preferences**: Isolated download history, language, and sidebar shortcuts stored in each client browser's `localStorage`.
- 📱 **Mobile Responsive & Bottom Navigation**: Adaptive layout for Desktop and dedicated Smartphone layout with top shortcuts scrollbar and bottom nav bar.

---

## 🚀 Running from Source

### Prerequisites
- Python 3.9 or higher.
- Installed dependencies (`yt-dlp`, `imageio_ffmpeg`).

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/RafaelParoni/Paroni-Downloader.git
   cd Paroni-Downloader
   ```
2. Install required packages:
   ```bash
   py -m pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   py server.py
   ```
4. Open your browser at `http://localhost:3000`.

---

## 🪟 Windows Setup (PyInstaller + Inno Setup)

Compile into a standalone Windows executable and create a setup wizard (`setup.exe`):

1. **Build Executable (`.exe`) with PyInstaller:**
   ```bash
   py -m PyInstaller --noconfirm paroni_downloader.spec
   ```
   *Generated executable will be saved in `dist/ParoniDownloaderServer.exe`.*

2. **Generate Windows Installer (`Setup.exe`) via Inno Setup:**
   - Open **Inno Setup Compiler**.
   - Load `installer_windows.iss`.
   - Click **Compile** (`Ctrl + F9`).
   - The final setup wizard `ParoniDownloader-Setup-v2.5.exe` is created in `installer_output/`.

---

## GNU/Linux Setup (.DEB Package & Auto-Installer)

Choose between two native installation methods for Linux:

### Option 1: Graphical `.DEB` Package (Ubuntu / Debian / Linux Mint / Pop!_OS)
1. Build the `.deb` package:
   ```bash
   chmod +x create_deb_package.sh
   ./create_deb_package.sh
   ```
2. The package **`paroni-downloader_2.5_all.deb`** will be generated.
3. Double-click the `.deb` file in your Linux file manager to open Ubuntu Software Center and click **Install**, or run:
   ```bash
   sudo dpkg -i paroni-downloader_2.5_all.deb
   ```

### Option 2: Shell Auto-Installer Script (Any Linux Distro)
1. Install with systemd daemon integration & desktop shortcut:
   ```bash
   chmod +x install_linux.sh
   sudo ./install_linux.sh
   ```
2. Check systemd service status:
   ```bash
   sudo systemctl status paroni-downloader
   ```
3. Uninstall from Linux:
   ```bash
   chmod +x uninstall_linux.sh
   sudo ./uninstall_linux.sh
   ```

---

## 👤 Author & Links

- **Author**: Rafael Paroni
- **GitHub**: [https://github.com/RafaelParoni/Paroni-Downloader](https://github.com/RafaelParoni/Paroni-Downloader)
- **Site**: [https://rafaelparoni.vercel.app/](https://rafaelparoni.vercel.app/)

---
*MIT License - Personal and educational use.*
