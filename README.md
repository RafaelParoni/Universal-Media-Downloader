# Universal Media Downloader

![Version](https://img.shields.io/badge/version-1.2.3-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows_10%2F11-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Universal Media Downloader** is a modern, lightweight, and easy-to-use desktop application designed to download videos and audio from the most popular social media and streaming platforms, all in one place.

## ✨ Features

- **Multi-Platform Support**: Download seamlessly from:
  - ▷ **YouTube**: High-quality videos or audio-only.
  - 🎵 **Spotify**: Tracks and songs converted to standard audio formats (MP3).
  - 📱 **TikTok**: Direct video downloads.
  - 📸 **Instagram**: Reels, posts, and videos.
- **Customizable Quality**: Choose your preferred resolution (1080p, 720p, 480p, 360p) or opt for "Best Quality".
- **Format Selection**: 
  - Video + Audio
  - Video Only
  - Audio Only
- **History Tab**: Keep track of all your downloads. View media details (Name, Service, Duration, Link, Location), open the downloaded folder directly, or delete items from history.
- **Multi-Language Support**: Fully translated into Portuguese, English, Spanish, Russian, Japanese, and Chinese.
- **Modern User Interface**: Built with `customtkinter` for a sleek, dark-themed, and responsive UI.

## 🚀 Installation (Windows)

You can download the compiled installer (`Universal_Media_Downloader_Setup.exe`) from the [Releases](#) section.

1. Download the latest `setup.exe`.
2. Run the installer and follow the instructions.
3. Open **Universal Media Downloader** from your desktop or start menu.

## 🛠️ Development & Building from Source

If you want to run the application from the source code or build your own executable:

### Prerequisites

Ensure you have Python 3.9+ installed and `pip` available on your system. 
You also need `ffmpeg` configured (the script automatically pulls `imageio-ffmpeg` to handle conversions).

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RafaelParoni/UniversalMediaDownloader.git
   cd UniversalMediaDownloader
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Required packages typically include: `customtkinter`, `yt-dlp`, `imageio-ffmpeg`, etc.*

3. **Run the application:**
   ```bash
   python youtube_downloader.py
   ```

### Building the Executable

To compile the application into a standalone Windows `.exe` using PyInstaller:

```bash
pyinstaller --noconfirm youtube_downloader.spec
```

To create an installer, use **Inno Setup** and compile the provided `youtube_downloader.iss` script.


## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
*Disclaimer: This tool is intended for personal use and for downloading content you own or have permission to use. Please respect the copyright policies of the respective platforms.*
