# Paroni Downloader

![Versão](https://img.shields.io/badge/versão-1.2.3-blue.svg)
![Plataforma](https://img.shields.io/badge/plataforma-Windows_10%2F11-lightgrey.svg)
![Licença](https://img.shields.io/badge/licença-MIT-green.svg)

O **Paroni Downloader** é um aplicativo de desktop moderno, leve e fácil de usar, projetado para baixar vídeos e áudios das redes sociais e plataformas de streaming mais populares, tudo em um só lugar.

## ✨ Recursos

- **Suporte Multiplataforma**: Baixe facilmente de:
  - ▷ **YouTube**: Vídeos em alta qualidade ou apenas o áudio.
  - 🎵 **Spotify**: Faixas e músicas convertidas para formatos de áudio padrão (MP3).
  - 📱 **TikTok**: Download direto de vídeos.
  - 📸 **Instagram**: Reels, posts e vídeos.
- **Qualidade Personalizável**: Escolha a resolução desejada (1080p, 720p, 480p, 360p) ou opte pela "Melhor Qualidade".
- **Seleção de Formato**: 
  - Vídeo + Áudio
  - Somente Áudio
  - Somente Vídeo
- **Aba de Histórico**: Mantenha o controle de todos os seus downloads. Visualize os detalhes da mídia (Nome, Serviço, Duração, Link, Local), abra a pasta do arquivo baixado diretamente ou exclua itens do histórico.
- **Suporte a Múltiplos Idiomas**: Totalmente traduzido para Português, Inglês, Espanhol, Russo, Japonês e Chinês.
- **Interface de Usuário Moderna**: Desenvolvido com `customtkinter` para uma interface elegante, com tema escuro e responsiva.

## 🚀 Instalação (Windows)

Você pode baixar o instalador compilado (`Universal_Media_Downloader_Setup.exe`) na seção [Releases](https://github.com/RafaelParoni/Universal-Media-Downloader/releases).

1. Baixe o `setup.exe` mais recente.
2. Execute o instalador e siga as instruções na tela.
3. Abra o **Paroni Downloader** pelo atalho na sua área de trabalho ou menu iniciar.

## 🛠️ Desenvolvimento e Compilação do Código-Fonte

Caso você queira rodar o aplicativo a partir do código-fonte ou compilar seu próprio executável:

### Pré-requisitos

Certifique-se de ter o Python 3.9+ instalado e o `pip` disponível no seu sistema. 
Você também precisa do `ffmpeg` configurado (o script puxa automaticamente o `imageio-ffmpeg` para lidar com as conversões internamente).

### Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/RafaelParoni/UniversalMediaDownloader.git
   cd UniversalMediaDownloader
   ```

2. **Instale as dependências necessárias:**
   ```bash
   pip install -r requirements.txt
   ```
   *Os pacotes necessários geralmente incluem: `customtkinter`, `yt-dlp`, `imageio-ffmpeg`, etc.*

3. **Execute o aplicativo:**
   ```bash
   python youtube_downloader.py
   ```

### Compilando o Executable

Para compilar o aplicativo em um `.exe` autônomo para Windows usando o PyInstaller:

```bash
pyinstaller --noconfirm youtube_downloader.spec
```

Para criar um instalador amigável, utilize o **Inno Setup** e compile o script `youtube_downloader.iss` fornecido na pasta.

## 📝 Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

---
*Aviso: Esta ferramenta destina-se ao uso pessoal e ao download de conteúdo que você possui ou tem permissão para usar. Por favor, respeite as políticas de direitos autorais das respectivas plataformas.*


