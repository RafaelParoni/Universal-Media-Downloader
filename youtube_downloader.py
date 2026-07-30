import os
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
import urllib.request
import urllib.error
import re
import json
import multiprocessing

try:
    import customtkinter as ctk
    import yt_dlp
    import imageio_ffmpeg
    from PIL import Image
except ImportError:
    import sys
    import subprocess
    if not getattr(sys, 'frozen', False):
        print("Instalando dependências...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter", "yt-dlp", "imageio-ffmpeg", "pillow"])
    import customtkinter as ctk
    import yt_dlp
    import imageio_ffmpeg
    from PIL import Image

import json
import base64
import io

try:
    from service_icons import ICONS_B64
except:
    ICONS_B64 = {}

try:
    import pywinstyles
except ImportError:
    pywinstyles = None

import ctypes

# Paleta de Cores (Suporte a Modo Claro e Escuro)
BG_COLOR = ("#e0e0e0", "#1c1c1c")       # Fundo principal (#e0e0e0 no modo claro, #1c1c1c no modo escuro)
SIDEBAR_COLOR = "transparent"  # Fundo da barra lateral transparente
CARD_COLOR = ("#f4f4f4", "#242424")     # Fundo dos "cards" arredondados
ENTRY_BG = ("#ffffff", "#2d2d2d")       # Fundo das caixas de texto
ACCENT_COLOR = "#004AAD"               # Azul Primário
ACCENT_CYAN = "#5DE0E6"                # Ciano Destaque
ACCENT_HOVER = "#003580"               # Azul Escuro Hover
BORDER_COLOR = ("#004AAD", "#5DE0E6")   # Cor da borda
TEXT_COLOR = ("#111111", "#FFFFFF")     # Texto escuro no modo claro, claro no modo escuro

def create_gradient_image(width, height, start_hex="#5DE0E6", end_hex="#004AAD"):
    """Cria uma imagem de gradiente linear horizontal 90deg de start_hex até end_hex."""
    try:
        w = max(1, int(width))
        h = max(1, int(height))
        
        def hex_to_rgb(hex_str):
            hex_str = hex_str.lstrip('#')
            return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
        
        r1, g1, b1 = hex_to_rgb(start_hex)
        r2, g2, b2 = hex_to_rgb(end_hex)
        
        img = Image.new("RGB", (w, 1))
        pixels = []
        for x in range(w):
            t = x / max(1, w - 1)
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            pixels.append((r, g, b))
        img.putdata(pixels)
        return img.resize((w, h), Image.Resampling.NEAREST)
    except Exception:
        return Image.new("RGB", (max(1, int(width)), max(1, int(height))), "#004AAD")

def apply_windows_blur(window):
    """Aplica o efeito Acrylic / Blur da DWM do Windows na janela principal."""
    if os.name != 'nt':
        return
    try:
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        if not hwnd:
            hwnd = window.winfo_id()

        class ACCENT_POLICY(ctypes.Structure):
            _fields_ = [
                ("AccentState", ctypes.c_int),
                ("AccentFlags", ctypes.c_int),
                ("GradientColor", ctypes.c_int),
                ("AnimationId", ctypes.c_int)
            ]

        class WINDOWCOMPOSITIONATTRIB_DATA(ctypes.Structure):
            _fields_ = [
                ("Attribute", ctypes.c_int),
                ("Data", ctypes.POINTER(ACCENT_POLICY)),
                ("SizeOfData", ctypes.c_size_t)
            ]

        accent = ACCENT_POLICY()
        accent.AccentState = 4  # ACCENT_ENABLE_ACRYLICBLURBEHIND
        accent.GradientColor = 0xAA004AAD  # Alpha + ABGR color tint

        data = WINDOWCOMPOSITIONATTRIB_DATA()
        data.Attribute = 19  # WCA_ACCENT_POLICY
        data.Data = ctypes.pointer(accent)
        data.SizeOfData = ctypes.sizeof(accent)

        ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.byref(data))
    except Exception:
        pass

# Configuração Base
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "config.json"

LANGUAGES = {
    "Português": {
        "title": "Paroni Downloader",
        "youtube": "Baixador do YouTube",
        "spotify": "Baixador do Spotify",
        "tiktok": "Baixador do TikTok",
        "instagram": "Baixador do Instagram",
        "twitter": "Baixador do Twitter",
        "reddit": "Baixador do Reddit",
        "pinterest": "Baixador do Pinterest",
        "facebook": "Baixador do Facebook",
        "kwai": "Baixador do Kwai",
        "vimeo": "Baixador do Vimeo",
        "twitch": "Baixador da Twitch",
        "soundcloud": "Baixador do SoundCloud",
        "bandcamp": "Baixador do Bandcamp",
        "rumble": "Baixador do Rumble",
        "bilibili": "Baixador do BiliBili",
        "others": "Todos os Serviços",
        "others_menu": "Todos os Serviços",
        "settings": "Configurações",
        "placeholder_yt": "Cole o link do vídeo do YouTube...",
        "placeholder_sp": "Cole o link da música do Spotify... (Apenas Áudio)",
        "placeholder_tk": "Cole o link do vídeo do TikTok...",
        "placeholder_ig": "Cole o link do Reels/Post do Instagram...",
        "placeholder_tw": "Cole o link do X/Twitter aqui...",
        "placeholder_re": "Cole o link do post do Reddit aqui...",
        "placeholder_pi": "Cole o link do Pin do Pinterest aqui...",
        "placeholder_fa": "Cole o link do vídeo do Facebook aqui...",
        "placeholder_kw": "Cole o link do vídeo do Kwai aqui...",
        "placeholder_vi": "Cole o link do vídeo do Vimeo aqui...",
        "placeholder_tw": "Cole o link do clipe/VOD da Twitch aqui...",
        "placeholder_so": "Cole o link da música do SoundCloud aqui... (Apenas Áudio)",
        "placeholder_ba": "Cole o link da música do Bandcamp aqui... (Apenas Áudio)",
        "placeholder_ru": "Cole o link do vídeo do Rumble aqui...",
        "placeholder_bi": "Cole o link do vídeo do BiliBili aqui...",
        "btn_download": "Baixar",
        "video_audio": "Vídeo + Áudio",
        "audio_only": "Apenas Áudio",
        "video_only": "Apenas Vídeo",
        "best_quality": "Melhor Qualidade",
        "select_folder": "Escolher Pasta de Download",
        "language_lbl": "Idioma do Aplicativo:",
        "resizable_window_lbl": "Permitir Redimensionar Janela",
        "save_settings": "Salvar Configurações",
        "empty_url": "Por favor, insira um link válido.",
        "downloading": "Baixando... (Pode demorar dependendo da internet)",
        "done": "Download concluído! Salvo na pasta designada.",
        "extracting": "Extraindo informações do Spotify...",
        "found": "Encontrado: {}. Buscando áudio...",
        "error_link": "Erro: Verifique o link ou a conexão.",
        "open_folder": "Abrir Pasta",
        "version": "Versão",
        "history": "Histórico",
        "media_name": "Nome da Mídia",
        "service": "Serviço",
        "duration": "Duração",
        "link": "Link",
        "location": "Local",
        "no_history": "Nenhum histórico disponível.",
        "delete": "Excluir"
    },
    "English": {
        "title": "Paroni Downloader",
        "youtube": "YouTube Downloader",
        "spotify": "Spotify Downloader",
        "tiktok": "TikTok Downloader",
        "instagram": "Instagram Downloader",
        "twitter": "Twitter Downloader",
        "reddit": "Reddit Downloader",
        "pinterest": "Pinterest Downloader",
        "facebook": "Facebook Downloader",
        "kwai": "Kwai Downloader",
        "vimeo": "Vimeo Downloader",
        "twitch": "Twitch Downloader",
        "soundcloud": "SoundCloud Downloader",
        "bandcamp": "Bandcamp Downloader",
        "rumble": "Rumble Downloader",
        "bilibili": "BiliBili Downloader",
        "others": "All Services",
        "others_menu": "All Services",
        "settings": "Settings",
        "placeholder_yt": "Paste YouTube video link here...",
        "placeholder_sp": "Paste Spotify track link here... (Audio Only)",
        "placeholder_tk": "Paste TikTok video link here...",
        "placeholder_ig": "Paste Instagram Reels/Post link here...",
        "placeholder_tw": "Paste X/Twitter link here...",
        "placeholder_re": "Paste Reddit post link here...",
        "placeholder_pi": "Paste Pinterest pin link here...",
        "placeholder_fa": "Paste Facebook video link here...",
        "placeholder_kw": "Paste Kwai video link here...",
        "placeholder_vi": "Paste Vimeo video link here...",
        "placeholder_tw": "Paste Twitch clip/VOD link here...",
        "placeholder_so": "Paste SoundCloud track link here... (Audio Only)",
        "placeholder_ba": "Paste Bandcamp track link here... (Audio Only)",
        "placeholder_ru": "Paste Rumble video link here...",
        "placeholder_bi": "Paste BiliBili video link here...",
        "btn_download": "Download",
        "video_audio": "Video + Audio",
        "audio_only": "Audio Only",
        "video_only": "Video Only",
        "best_quality": "Best Quality",
        "select_folder": "Choose Download Folder",
        "language_lbl": "App Language:",
        "resizable_window_lbl": "Allow Window Resizing",
        "save_settings": "Save Settings",
        "empty_url": "Please enter a valid link.",
        "downloading": "Downloading... (May take a while depending on internet)",
        "done": "Download finished! Saved to destination folder.",
        "extracting": "Extracting Spotify info...",
        "found": "Found: {}. Fetching audio...",
        "error_link": "Error: Check your link or connection.",
        "open_folder": "Open Folder",
        "version": "Version",
        "history": "History",
        "media_name": "Media Name",
        "service": "Service",
        "duration": "Duration",
        "link": "Link",
        "location": "Location",
        "no_history": "No history available.",
        "delete": "Delete"
    },
    "Español": {
        "title": "Paroni Downloader",
        "youtube": "Descargador de YouTube",
        "spotify": "Descargador de Spotify",
        "tiktok": "Descargador de TikTok",
        "instagram": "Descargador de Instagram",
        "twitter": "Descargador de Twitter",
        "reddit": "Descargador de Reddit",
        "pinterest": "Descargador de Pinterest",
        "facebook": "Descargador de Facebook",
        "kwai": "Descargador de Kwai",
        "vimeo": "Descargador de Vimeo",
        "twitch": "Descargador de Twitch",
        "soundcloud": "Descargador de SoundCloud",
        "bandcamp": "Descargador de Bandcamp",
        "rumble": "Descargador de Rumble",
        "bilibili": "Descargador de BiliBili",
        "others": "Otros",
        "others_menu": "Otros Servicios",
        "settings": "Ajustes",
        "placeholder_yt": "Pega el enlace del video de YouTube aquí...",
        "placeholder_sp": "Pega el enlace de la pista de Spotify... (Solo Audio)",
        "placeholder_tk": "Pega el enlace del video de TikTok aquí...",
        "placeholder_ig": "Pega el enlace de Reels/Post de Instagram...",
        "placeholder_tw": "Pega el enlace de X/Twitter aquí...",
        "placeholder_re": "Pega el enlace del post de Reddit aquí...",
        "placeholder_pi": "Pega el enlace del Pin de Pinterest aquí...",
        "placeholder_fa": "Pega el enlace del video de Facebook aquí...",
        "placeholder_kw": "Pega el enlace del video de Kwai aquí...",
        "placeholder_vi": "Pega el enlace del video de Vimeo aquí...",
        "placeholder_tw": "Pega el enlace del clip/VOD de Twitch aquí...",
        "placeholder_so": "Pega el enlace de la pista de SoundCloud... (Solo Audio)",
        "placeholder_ba": "Pega el enlace de la pista de Bandcamp... (Solo Audio)",
        "placeholder_ru": "Pega el enlace del video de Rumble aquí...",
        "placeholder_bi": "Pega el enlace del video de BiliBili aquí...",
        "btn_download": "Descargar",
        "video_audio": "Video + Audio",
        "audio_only": "Solo Audio",
        "video_only": "Solo Video",
        "best_quality": "Mejor Calidad",
        "select_folder": "Elegir Carpeta de Descarga",
        "language_lbl": "Idioma de la App:",
        "save_settings": "Guardar Ajustes",
        "empty_url": "Por favor, ingresa un enlace válido.",
        "downloading": "Descargando... (Puede tardar dependiendo del internet)",
        "done": "¡Descarga completada! Guardado en la carpeta.",
        "extracting": "Extrayendo info de Spotify...",
        "found": "Encontrado: {}. Buscando audio...",
        "error_link": "Error: Verifica tu enlace o conexión.",
        "open_folder": "Abrir Carpeta",
        "version": "Versión",
        "history": "Historial",
        "media_name": "Nombre del Medio",
        "service": "Servicio",
        "duration": "Duración",
        "link": "Enlace",
        "location": "Ubicación",
        "no_history": "No hay historial disponible.",
        "delete": "Eliminar"
    },
    "Русский": {
        "title": "Paroni Downloader",
        "youtube": "Загрузчик YouTube",
        "spotify": "Загрузчик Spotify",
        "tiktok": "Загрузчик TikTok",
        "instagram": "Загрузчик Instagram",
        "twitter": "Загрузчик Twitter",
        "reddit": "Загрузчик Reddit",
        "pinterest": "Загрузчик Pinterest",
        "facebook": "Загрузчик Facebook",
        "kwai": "Загрузчик Kwai",
        "vimeo": "Загрузчик Vimeo",
        "twitch": "Загрузчик Twitch",
        "soundcloud": "Загрузчик SoundCloud",
        "bandcamp": "Загрузчик Bandcamp",
        "rumble": "Загрузчик Rumble",
        "bilibili": "Загрузчик BiliBili",
        "others": "Другие",
        "others_menu": "Другие сервисы",
        "settings": "Настройки",
        "placeholder_yt": "Вставьте ссылку на видео YouTube...",
        "placeholder_sp": "Вставьте ссылку на трек Spotify... (Только аудио)",
        "placeholder_tk": "Вставьте ссылку на видео TikTok...",
        "placeholder_ig": "Вставьте ссылку на Reels/Post Instagram...",
        "placeholder_tw": "Вставьте ссылку на X/Twitter...",
        "placeholder_re": "Вставьте ссылку на пост Reddit...",
        "placeholder_pi": "Вставьте ссылку на пин Pinterest...",
        "placeholder_fa": "Вставьте ссылку на видео Facebook...",
        "placeholder_kw": "Вставьте ссылку на видео Kwai...",
        "placeholder_vi": "Вставьте ссылку на видео Vimeo...",
        "placeholder_tw": "Вставьте ссылку на клип/VOD Twitch...",
        "placeholder_so": "Вставьте ссылку на трек SoundCloud... (Только аудио)",
        "placeholder_ba": "Вставьте ссылку на трек Bandcamp... (Только аудио)",
        "placeholder_ru": "Вставьте ссылку на видео Rumble...",
        "placeholder_bi": "Вставьте ссылку на видео BiliBili...",
        "btn_download": "Скачать",
        "video_audio": "Видео + Аудио",
        "audio_only": "Только Аудио",
        "video_only": "Только Видео",
        "best_quality": "Лучшее Качество",
        "select_folder": "Выбрать Папку",
        "language_lbl": "Язык Приложения:",
        "save_settings": "Сохранить",
        "empty_url": "Пожалуйста, введите правильную ссылку.",
        "downloading": "Скачивание... (Может занять время)",
        "done": "Готово! Сохранено в папку загрузок.",
        "extracting": "Извлечение Spotify...",
        "found": "Найдено: {}. Поиск аудио...",
        "error_link": "Ошибка: Проверьте ссылку или интернет.",
        "open_folder": "Открыть Папку",
        "version": "Версия",
        "history": "История",
        "media_name": "Название Медиа",
        "service": "Сервис",
        "duration": "Продолжительность",
        "link": "Ссылка",
        "location": "Расположение",
        "no_history": "История недоступна.",
        "delete": "Удалить"
    },
    "日本語": {
        "title": "Paroni Downloader",
        "youtube": "YouTube ダウンローダー",
        "spotify": "Spotify ダウンローダー",
        "tiktok": "TikTok ダウンローダー",
        "instagram": "Instagram ダウンローダー",
        "twitter": "Twitter ダウンローダー",
        "reddit": "Reddit ダウンローダー",
        "pinterest": "Pinterest ダウンローダー",
        "facebook": "Facebook ダウンローダー",
        "kwai": "Kwai ダウンローダー",
        "vimeo": "Vimeo ダウンローダー",
        "twitch": "Twitch ダウンローダー",
        "soundcloud": "SoundCloud ダウンローダー",
        "bandcamp": "Bandcamp ダウンローダー",
        "rumble": "Rumble ダウンローダー",
        "bilibili": "BiliBili ダウンローダー",
        "others": "その他",
        "others_menu": "その他のサービス",
        "settings": "設定",
        "placeholder_yt": "YouTubeの動画リンクを貼り付け...",
        "placeholder_sp": "Spotifyのリンクを貼り付け... (音声のみ)",
        "placeholder_tk": "TikTokの動画リンクを貼り付け...",
        "placeholder_ig": "InstagramのReels/Postリンクを貼り付け...",
        "placeholder_tw": "X/Twitterのリンクを貼り付け...",
        "placeholder_re": "Redditの投稿リンクを貼り付け...",
        "placeholder_pi": "Pinterestのピンリンクを貼り付け...",
        "placeholder_fa": "Facebookの動画リンクを貼り付け...",
        "placeholder_kw": "Kwaiの動画リンクを貼り付け...",
        "placeholder_vi": "Vimeoの動画リンクを貼り付け...",
        "placeholder_tw": "Twitchのクリップ/VODリンクを貼り付け...",
        "placeholder_so": "SoundCloudのトラックリンクを貼り付け... (音声のみ)",
        "placeholder_ba": "Bandcampのトラックリンクを貼り付け... (音声のみ)",
        "placeholder_ru": "Rumbleの動画リンクを貼り付け...",
        "placeholder_bi": "BiliBiliの動画リンクを貼り付け...",
        "btn_download": "ダウンロード",
        "video_audio": "ビデオ + 音声",
        "audio_only": "音声のみ",
        "video_only": "ビデオのみ",
        "best_quality": "最高画質",
        "select_folder": "保存先フォルダを選択",
        "language_lbl": "アプリの言語:",
        "resizable_window_lbl": "ウィンドウのサイズ変更を許可",
        "save_settings": "設定を保存",
        "empty_url": "有効なリンクを入力してください。",
        "downloading": "ダウンロード中... (回線により時間がかかります)",
        "done": "完了！ フォルダに保存されました。",
        "extracting": "Spotifyの情報を抽出中...",
        "found": "発見: {}。音声を検索中...",
        "error_link": "エラー: リンクか接続を確認してください。",
        "open_folder": "フォルダを開く",
        "version": "バージョン",
        "history": "履歴",
        "media_name": "メディア名",
        "service": "サービス",
        "duration": "時間",
        "link": "リンク",
        "location": "場所",
        "no_history": "履歴はありません。",
        "delete": "削除"
    },
    "中文": {
        "title": "Paroni Downloader",
        "youtube": "YouTube 下载器",
        "spotify": "Spotify 下载器",
        "tiktok": "TikTok 下载器",
        "instagram": "Instagram 下载器",
        "twitter": "Twitter 下载器",
        "reddit": "Reddit 下载器",
        "pinterest": "Pinterest 下载器",
        "facebook": "Facebook 下载器",
        "kwai": "Kwai 下载器",
        "vimeo": "Vimeo 下载器",
        "twitch": "Twitch 下载器",
        "soundcloud": "SoundCloud 下载器",
        "bandcamp": "Bandcamp 下载器",
        "rumble": "Rumble 下载器",
        "bilibili": "BiliBili 下载器",
        "others": "其他",
        "others_menu": "其他服务",
        "settings": "设置",
        "placeholder_yt": "在此粘贴YouTube视频链接...",
        "placeholder_sp": "在此粘贴Spotify歌曲链接... (仅音频)",
        "placeholder_tk": "在此粘贴TikTok视频链接...",
        "placeholder_ig": "在此粘贴Instagram Reels/Post链接...",
        "placeholder_tw": "在此粘贴X/Twitter链接...",
        "placeholder_re": "在此粘贴Reddit帖子链接...",
        "placeholder_pi": "在此粘贴Pinterest的Pin链接...",
        "placeholder_fa": "在此粘贴Facebook视频链接...",
        "placeholder_kw": "在此粘贴Kwai视频链接...",
        "placeholder_vi": "在此粘贴Vimeo视频链接...",
        "placeholder_tw": "在此粘贴Twitch剪辑/VOD链接...",
        "placeholder_so": "在此粘贴SoundCloud曲目链接... (仅音频)",
        "placeholder_ba": "在此粘贴Bandcamp曲目链接... (仅音频)",
        "placeholder_ru": "在此粘贴Rumble视频链接...",
        "placeholder_bi": "在此粘贴BiliBili视频链接...",
        "btn_download": "下载",
        "video_audio": "视频 + 音频",
        "audio_only": "仅音频",
        "video_only": "仅视频",
        "best_quality": "最佳质量",
        "select_folder": "选择下载文件夹",
        "language_lbl": "应用语言:",
        "resizable_window_lbl": "允许调整窗口大小",
        "save_settings": "保存设置",
        "empty_url": "请输入有效的链接。",
        "downloading": "下载中... (根据网络可能需要一些时间)",
        "done": "下载完成！ 已保存到目标文件夹。",
        "extracting": "正在提取Spotify信息...",
        "found": "找到: {}。正在获取音频...",
        "error_link": "错误：请检查您的链接或网络连接。",
        "open_folder": "打开文件夹",
        "version": "版本",
        "history": "历史",
        "media_name": "媒体名称",
        "service": "服务",
        "duration": "持续时间",
        "link": "链接",
        "location": "位置",
        "no_history": "没有可用的历史记录。",
        "delete": "删除"
    }
}


class OthersFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, app_ref):
        super().__init__(master, corner_radius=0, fg_color=BG_COLOR)
        self.grid_columnconfigure(0, weight=1)
        self.app_ref = app_ref

        # Card Central
        self.card = ctk.CTkFrame(self, fg_color="transparent")
        self.card.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")

        fonte_titulo = ctk.CTkFont(size=24, weight="bold")

        self.title_label = ctk.CTkLabel(self.card, text="Todos os Serviços", font=fonte_titulo, text_color=TEXT_COLOR)
        self.title_label.grid(row=0, column=0, pady=(40, 30))

        # services = (Name, Command, VideoSupport, AudioSupport, IconKey)
        services = [
            ("YouTube", app_ref.show_youtube, True, True, "YouTube"),
            ("Spotify", app_ref.show_spotify, False, True, "Spotify"),
            ("TikTok", app_ref.show_tiktok, True, True, "TikTok"),
            ("Instagram", app_ref.show_instagram, True, True, "Instagram"),
            ("Twitter (X)", app_ref.show_twitter, True, True, "Twitter"),
            ("Reddit", app_ref.show_reddit, True, True, "Reddit"),
            ("Pinterest", app_ref.show_pinterest, True, True, "Pinterest"),
            ("Facebook", app_ref.show_facebook, True, True, "Facebook"),
            ("Kwai", app_ref.show_kwai, True, True, "Kwai"),
            ("Vimeo", app_ref.show_vimeo, True, True, "Vimeo"),
            ("Twitch", app_ref.show_twitch, True, True, "Twitch"),
            ("SoundCloud", app_ref.show_soundcloud, False, True, "SoundCloud"),
            ("Bandcamp", app_ref.show_bandcamp, False, True, "Bandcamp"),
            ("BiliBili", app_ref.show_bilibili, True, True, "BiliBili")
        ]

        row = 1
        col = 0
        self.service_cards = []
        for text, command, has_video, has_audio, icon_key in services:
            # Create a small nested frame for each service card
            srv_card = ctk.CTkFrame(self.card, fg_color=ENTRY_BG, corner_radius=15, cursor="hand2", width=140, height=160)
            srv_card.grid(row=row, column=col, padx=15, pady=15)
            srv_card.grid_propagate(False)
            srv_card.grid_columnconfigure(0, weight=1)
            
            # Icon
            img_ctk = None
            if icon_key in ICONS_B64:
                try:
                    img_data = base64.b64decode(ICONS_B64[icon_key])
                    img = Image.open(io.BytesIO(img_data)).resize((48, 48), Image.Resampling.LANCZOS)
                    img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(48, 48))
                except Exception as e:
                    print(f"Error loading icon for {icon_key}: {e}")

            if img_ctk:
                icon_display = ctk.CTkLabel(srv_card, text="", image=img_ctk, cursor="hand2")
                icon_display.grid(row=0, column=0, pady=(15, 5))
            else:
                icon_display = ctk.CTkLabel(srv_card, text="🔌", font=ctk.CTkFont(size=36), cursor="hand2")
                icon_display.grid(row=0, column=0, pady=(15, 5))
                
            # Name
            name_lbl = ctk.CTkLabel(srv_card, text=text, font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT_COLOR, cursor="hand2")
            name_lbl.grid(row=1, column=0, pady=(0, 5))
            
            # Indicators
            ind_frame = ctk.CTkFrame(srv_card, fg_color="transparent", cursor="hand2")
            ind_frame.grid(row=2, column=0, pady=(0, 15))
            
            if has_video and has_audio:
                ind_text = "Vídeo e Áudio Suportado"
            elif has_video:
                ind_text = "Vídeo Suportado"
            elif has_audio:
                ind_text = "Apenas Áudio Suportado"
            else:
                ind_text = "Não Suportado"
                
            ind_lbl = ctk.CTkLabel(ind_frame, text=ind_text, font=ctk.CTkFont(size=11), text_color=("black", "white"), cursor="hand2")
            ind_lbl.grid(row=0, column=0, padx=5)

            # --- Event Binding ---
            def on_enter(e, c=srv_card):
                c.configure(fg_color=ACCENT_HOVER)
                
            def on_leave(e, c=srv_card):
                c.configure(fg_color=ENTRY_BG)
                
            def on_click(e, cmd=command):
                cmd()

            elements = [srv_card, icon_display, name_lbl, ind_frame, ind_lbl]
            for elem in elements:
                elem.bind("<Enter>", on_enter)
                elem.bind("<Leave>", on_leave)
                elem.bind("<Button-1>", on_click)

            self.service_cards.append(srv_card)
        
        self.current_cols = 0
        self.bind("<Configure>", self.reorganize_cards, add="+")

        self.translate_ui(app_ref.config.get("language", "Português"))

    def reorganize_cards(self, event):
        if event.widget == self:
            available_width = event.width
            # Largura do card é 140. Padding left+right é 15+15=30. Total por card = 170.
            # Adicionar um pequeno espaço extra de margem para evitar aperto no scroll
            cols = max(1, (available_width - 80) // 170) 
            
            if getattr(self, 'current_cols', 0) != cols:
                self.current_cols = cols
                self.title_label.grid(row=0, column=0, columnspan=cols, pady=(40, 30))
                
                # Reseta as larguras das colunas e define as ativas
                for i in range(20):
                    self.card.grid_columnconfigure(i, weight=0)
                for i in range(cols):
                    self.card.grid_columnconfigure(i, weight=1)
                    
                # Reorganiza o grid de cada card baseando-se no limite de colunas
                for idx, card in enumerate(self.service_cards):
                    r = 1 + (idx // cols)
                    c = idx % cols
                    card.grid(row=r, column=c, padx=15, pady=15)

    def translate_ui(self, lang):
        t = LANGUAGES.get(lang, LANGUAGES["Português"])
        try:
            self.title_label.configure(text=t.get("others_menu", "Todos os Serviços"))
        except:
            pass

class HistoryFrame(ctk.CTkFrame):

    def __init__(self, master, app_ref):
        super().__init__(master, corner_radius=0, fg_color=BG_COLOR)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.app_ref = app_ref

        # Card Central
        self.card = ctk.CTkFrame(self, fg_color="transparent")
        self.card.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_rowconfigure(1, weight=1)

        fonte_titulo = ctk.CTkFont(size=24, weight="bold")
        self.fonte_texto = ctk.CTkFont(size=14)

        self.title_label = ctk.CTkLabel(self.card, text="Histórico", font=fonte_titulo, text_color=TEXT_COLOR)
        self.title_label.grid(row=0, column=0, pady=(40, 20))

        # Scrollable Frame para os itens
        self.scroll_frame = ctk.CTkScrollableFrame(self.card, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        self.no_history_label = ctk.CTkLabel(self.scroll_frame, text="", font=self.fonte_texto, text_color="#AAAAAA")
        self.no_history_label.grid(row=0, column=0, pady=50)

        self.history_items = []
        self.translate_ui(self.app_ref.config.get("language", "Português"))
        self.load_history(self.app_ref.config.get("history", []))

    def translate_ui(self, lang):
        t = LANGUAGES.get(lang, LANGUAGES["Português"])
        self.title_label.configure(text=t.get("history", "Histórico"))
        self.no_history_label.configure(text=t.get("no_history", "Nenhum histórico disponível."))
        # Atualizar labels dos itens existentes, se necessário
        for item_frame in self.history_items:
            for widget in item_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget.cget("text").startswith(t.get("media_name", "Nome da Mídia")):
                   pass # labels are static for now

    def add_item(self, entry):
        media_name = entry.get('name', '')
        service = entry.get('service', '')
        duration = entry.get('duration', '')
        link = entry.get('link', '')
        path = entry.get('path', '')
        
        t = LANGUAGES.get(self.app_ref.config.get("language", "Português"), LANGUAGES["Português"])
        
        self.no_history_label.grid_remove()
        
        item_frame = ctk.CTkFrame(self.scroll_frame, fg_color=ENTRY_BG, corner_radius=15, border_color=BORDER_COLOR, border_width=1)
        item_frame.grid(row=len(self.history_items) + 1, column=0, pady=5, padx=5, sticky="ew")
        item_frame.grid_columnconfigure(0, weight=1)
        
        info_text = f"[{service.upper()}] {media_name}\n"
        if duration:
            info_text += f"{t.get('duration', 'Duração')}: {duration} | "
        info_text += f"{t.get('location', 'Local')}: {os.path.basename(path)}"
        
        lbl_info = ctk.CTkLabel(item_frame, text=info_text, font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT_COLOR, justify="left", anchor="w")
        lbl_info.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        lbl_link = ctk.CTkLabel(item_frame, text=link, font=ctk.CTkFont(size=12), text_color="#AAAAAA", justify="left", anchor="w")
        lbl_link.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="w")
        
        # Botão para abrir o local
        btn_open = ctk.CTkButton(
            item_frame, text=t.get("open_folder", "Abrir Pasta"),
            command=lambda p=path: self.open_folder(p),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER, corner_radius=10, width=100, height=30
        )
        btn_open.grid(row=0, column=1, rowspan=2, padx=15, pady=15)
        
        # Botão para deletar
        btn_delete = ctk.CTkButton(
            item_frame, text=t.get("delete", "Excluir"),
            command=lambda e=entry: self.delete_history_item(e),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#D9534F", hover_color="#C9302C", corner_radius=10, width=80, height=30
        )
        btn_delete.grid(row=0, column=2, rowspan=2, padx=(0, 15), pady=15)
        
        self.history_items.append(item_frame)

    def load_history(self, history_list):
        for item in self.history_items:
            item.destroy()
        self.history_items.clear()
        
        if not history_list:
            self.no_history_label.grid()
        else:
            self.no_history_label.grid_remove()
            # Carregar em ordem reversa (mais recentes primeiro)
            for entry in reversed(history_list):
                self.add_item(entry)

    def delete_history_item(self, entry):
        history = self.app_ref.config.get("history", [])
        if entry in history:
            history.remove(entry)
            self.app_ref.save_config()
            self.load_history(history)

    def open_folder(self, file_path):
        folder = os.path.dirname(file_path) if os.path.isfile(file_path) else file_path
        if os.path.exists(folder):
            if os.name == 'nt':
                os.startfile(folder)
            else:
                import sys
                import subprocess
                if sys.platform == 'darwin':
                    subprocess.Popen(['open', folder])
                else:
                    subprocess.Popen(['xdg-open', folder])


class SettingsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, app_ref):
        # Atualização Visual
        super().__init__(master, corner_radius=0, fg_color=BG_COLOR)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.app_ref = app_ref

        # Card Central
        self.card = ctk.CTkFrame(self, fg_color="transparent")
        self.card.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        self.card.grid_columnconfigure(0, weight=1)

        fonte_titulo = ctk.CTkFont(size=24, weight="bold")
        self.fonte_texto = ctk.CTkFont(size=14)

        self.title_label = ctk.CTkLabel(self.card, text="Configurações", font=fonte_titulo, text_color=TEXT_COLOR)
        self.title_label.grid(row=0, column=0, pady=(40, 30))

        # Folder selection
        self.folder_var = ctk.StringVar(value=self.app_ref.config.get("download_folder", ""))
        self.btn_folder = ctk.CTkButton(
            self.card, text="Escolher Pasta de Download", 
            command=self.select_folder, font=self.fonte_texto,
            fg_color=ENTRY_BG, hover_color="#2A2C3F", text_color=TEXT_COLOR,
            corner_radius=15, border_color=ACCENT_COLOR, border_width=1, height=40
        )
        self.btn_folder.grid(row=1, column=0, pady=(10, 5))
        
        self.lbl_folder = ctk.CTkLabel(self.card, textvariable=self.folder_var, font=ctk.CTkFont(size=12), text_color="gray")
        self.lbl_folder.grid(row=2, column=0, pady=(0, 20))

        # Language selection
        self.lbl_lang = ctk.CTkLabel(self.card, text="Idioma do Aplicativo:", font=self.fonte_texto, text_color=TEXT_COLOR)
        self.lbl_lang.grid(row=3, column=0, pady=(10, 5))

        self.lang_var = ctk.StringVar(value=self.app_ref.config.get("language", "Português"))
        self.menu_lang = ctk.CTkOptionMenu(
            self.card, values=list(LANGUAGES.keys()), variable=self.lang_var, 
            command=self.change_language, font=self.fonte_texto,
            fg_color=ENTRY_BG, button_color=ENTRY_BG, button_hover_color="#2A2C3F",
            dropdown_fg_color=ENTRY_BG, dropdown_hover_color=ACCENT_HOVER, dropdown_text_color=TEXT_COLOR, text_color=TEXT_COLOR,
            corner_radius=10, height=35
        )
        self.menu_lang.grid(row=4, column=0, pady=(0, 20))

        # Shortcuts selection
        self.lbl_shortcuts = ctk.CTkLabel(self.card, text="Atalhos da Barra Lateral:", font=self.fonte_texto, text_color=TEXT_COLOR)
        self.lbl_shortcuts.grid(row=5, column=0, pady=(10, 5))
        
        self.shortcuts_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.shortcuts_frame.grid(row=6, column=0, pady=(0, 20))
        
        available_services = list(self.app_ref.SERVICES_INFO.keys())
        current_shortcuts = self.app_ref.config.get("shortcuts", ["youtube", "spotify", "tiktok", "instagram"])
        self.shortcut_vars = []
        for i in range(4):
            val = current_shortcuts[i] if i < len(current_shortcuts) else available_services[0]
            var = ctk.StringVar(value=val)
            self.shortcut_vars.append(var)
            
            menu = ctk.CTkOptionMenu(
                self.shortcuts_frame, values=available_services, variable=var,
                font=self.fonte_texto, fg_color=ENTRY_BG, button_color=ENTRY_BG, button_hover_color="#2A2C3F",
                dropdown_fg_color=ENTRY_BG, dropdown_hover_color=ACCENT_HOVER, dropdown_text_color=TEXT_COLOR, text_color=TEXT_COLOR,
                corner_radius=10, height=35, width=150
            )
            menu.grid(row=i//2, column=i%2, padx=10, pady=5)

        # Theme selection
        self.lbl_theme = ctk.CTkLabel(self.card, text="Tema do Aplicativo:", font=self.fonte_texto, text_color=TEXT_COLOR)
        self.lbl_theme.grid(row=7, column=0, pady=(10, 5))

        current_theme = self.app_ref.config.get("theme", "system")
        theme_map = {"system": "Automático", "dark": "Escuro", "light": "Claro"}
        self.theme_var = ctk.StringVar(value=theme_map.get(current_theme, "Automático"))
        self.menu_theme = ctk.CTkOptionMenu(
            self.card, values=["Automático", "Escuro", "Claro"], variable=self.theme_var, 
            command=self.change_theme, font=self.fonte_texto,
            fg_color=ENTRY_BG, button_color=ENTRY_BG, button_hover_color="#2A2C3F",
            dropdown_fg_color=ENTRY_BG, dropdown_hover_color=ACCENT_HOVER, dropdown_text_color=TEXT_COLOR, text_color=TEXT_COLOR,
            corner_radius=10, height=35
        )
        self.menu_theme.grid(row=8, column=0, pady=(0, 20))

        # Resizable Window Option
        self.resizable_window_var = ctk.BooleanVar(value=self.app_ref.config.get("resizable_window", False))
        self.switch_resize = ctk.CTkSwitch(
            self.card, text="Permitir Redimensionar Janela",
            variable=self.resizable_window_var,
            font=self.fonte_texto, text_color=TEXT_COLOR,
            progress_color=ACCENT_COLOR, button_color="#DDDDDD", button_hover_color="#FFFFFF"
        )
        self.switch_resize.grid(row=9, column=0, pady=(0, 30))

        # Save button
        self.btn_save = ctk.CTkButton(
            self.card, text="Salvar Configurações", 
            command=self.save_settings, font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER, corner_radius=20, height=45, width=220
        )
        self.btn_save.grid(row=10, column=0, pady=(10, 10))
        
        self.status_label = ctk.CTkLabel(self.card, text="", font=ctk.CTkFont(size=13))
        self.status_label.grid(row=11, column=0, pady=(0, 20))

        self.translate_ui(self.lang_var.get())

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)
            
    def change_language(self, new_lang):
        self.translate_ui(new_lang)
        self.app_ref.apply_translations(new_lang)

    def change_theme(self, new_theme_str):
        reverse_map = {"Automático": "system", "Escuro": "dark", "Claro": "light"}
        theme_val = reverse_map.get(new_theme_str, "system")
        ctk.set_appearance_mode(theme_val)
        self.app_ref.config["theme"] = theme_val
        self.app_ref.save_config()

    def translate_ui(self, lang):
        t = LANGUAGES.get(lang, LANGUAGES["Português"])
        try:
            self.title_label.configure(text=t["settings"])
            self.btn_folder.configure(text=t["select_folder"])
            self.lbl_lang.configure(text=t["language_lbl"])
            self.lbl_shortcuts.configure(text=t.get("shortcuts_lbl", "Atalhos da Barra Lateral:"))
            self.lbl_theme.configure(text=t.get("theme_lbl", "Tema do Aplicativo:"))
            self.btn_save.configure(text=t["save_settings"])
            self.switch_resize.configure(text=t.get("resizable_window_lbl", "Allow Window Resizing"))
        except:
            pass

    def save_settings(self):
        self.app_ref.config["download_folder"] = self.folder_var.get()
        self.app_ref.config["language"] = self.lang_var.get()
        is_resizable = self.resizable_window_var.get()
        self.app_ref.config["resizable_window"] = is_resizable
        
        # Save shortcuts
        new_shortcuts = [var.get() for var in self.shortcut_vars]
        self.app_ref.config["shortcuts"] = new_shortcuts
        
        self.app_ref.save_config()
        self.app_ref.resizable(is_resizable, is_resizable)
        self.app_ref.update_sidebar_shortcuts()
        
        self.status_label.configure(text="Configurações Salvas!", text_color="#00FF00")
        
        # Ocultar mensagem após 3 segundos
        self.after(3000, lambda: self.status_label.configure(text=""))

class DownloaderFrame(ctk.CTkFrame):
    def __init__(self, master, app_ref, title_key, placeholder_key, audio_only=False):
        super().__init__(master, corner_radius=0, fg_color=BG_COLOR)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.app_ref = app_ref
        self.title_key = title_key
        self.placeholder_key = placeholder_key
        self.audio_only = audio_only

        # Card Central
        self.card = ctk.CTkFrame(self, fg_color="transparent")
        self.card.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        self.card.grid_columnconfigure(0, weight=1)

        fonte_titulo = ctk.CTkFont(size=24, weight="bold")
        self.fonte_texto = ctk.CTkFont(size=14)

        self.title_label = ctk.CTkLabel(self.card, text="", font=fonte_titulo, text_color=TEXT_COLOR)
        self.title_label.grid(row=0, column=0, pady=(40, 20))

        self.url_entry = ctk.CTkEntry(
            self.card, 
            width=500, 
            height=45,
            font=self.fonte_texto,
            fg_color=ENTRY_BG,
            border_color=BORDER_COLOR,
            border_width=1,
            corner_radius=20,
            text_color=TEXT_COLOR
        )
        self.url_entry.grid(row=1, column=0, pady=(0, 25))

        # --- Frame de Opções (Formato e Qualidade) ---
        self.options_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.options_frame.grid(row=2, column=0, pady=(0, 25))

        self.type_var = ctk.StringVar()
        self.type_menu = ctk.CTkOptionMenu(
            self.options_frame, 
            variable=self.type_var,
            font=self.fonte_texto,
            width=200, height=35, corner_radius=15,
            fg_color=ENTRY_BG, button_color=ENTRY_BG, button_hover_color="#2A2C3F", dropdown_fg_color=ENTRY_BG, text_color=TEXT_COLOR
        )
        self.type_menu.grid(row=0, column=0, padx=15)
        
        if self.audio_only:
            self.type_menu.configure(state="disabled")

        self.quality_var = ctk.StringVar()
        self.quality_menu = ctk.CTkOptionMenu(
            self.options_frame, 
            variable=self.quality_var,
            font=self.fonte_texto,
            width=200, height=35, corner_radius=15,
            fg_color=ENTRY_BG, button_color=ENTRY_BG, button_hover_color="#2A2C3F", dropdown_fg_color=ENTRY_BG, text_color=TEXT_COLOR
        )
        self.quality_menu.grid(row=0, column=1, padx=15)
        # ---------------------------------------------

        self.download_btn = ctk.CTkButton(
            self.card, 
            text="", 
            command=self.start_download, 
            font=ctk.CTkFont(size=16, weight="bold"), 
            height=50, width=440,
            corner_radius=25,
            fg_color=ACCENT_COLOR,
            hover_color=ACCENT_HOVER,
            text_color="#FFFFFF"
        )
        self.download_btn.grid(row=3, column=0, pady=(10, 20))

        self.progress_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.progress_frame.grid(row=4, column=0, pady=(0, 10), sticky="ew", padx=80)
        self.progress_frame.grid_columnconfigure(0, weight=1)
        self.progress_frame.grid_remove()

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, progress_color=ACCENT_COLOR, height=10)
        self.progress_bar.grid(row=0, column=0, sticky="ew", padx=(0, 15))
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(self.progress_frame, text="0%", font=ctk.CTkFont(size=13, weight="bold"))
        self.progress_label.grid(row=0, column=1)

        self.status_label = ctk.CTkLabel(self.card, text="", font=ctk.CTkFont(size=13))
        self.status_label.grid(row=5, column=0, pady=(0, 10))

        self.open_folder_btn = ctk.CTkButton(
            self.card,
            text="",
            command=self.open_download_folder,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, width=200,
            corner_radius=20,
            fg_color="#27ae60",
            hover_color="#2ecc71",
            text_color="#FFFFFF"
        )
        self.open_folder_btn.grid(row=6, column=0, pady=(0, 10))
        self.open_folder_btn.grid_remove()

        self.filename_label = ctk.CTkLabel(self.card, text="", font=ctk.CTkFont(size=14, weight="bold"), text_color="#AAAAAA", wraplength=400)
        self.filename_label.grid(row=7, column=0, pady=(0, 20))
        self.filename_label.grid_remove()

        self.translate_ui(self.app_ref.config.get("language", "Português"))

    def translate_ui(self, lang):
        t = LANGUAGES.get(lang, LANGUAGES["Português"])
        
        self.title_label.configure(text=t[self.title_key])
        self.url_entry.configure(placeholder_text=t[self.placeholder_key])
        self.download_btn.configure(text=t["btn_download"])
        
        if hasattr(self, 'open_folder_btn'):
            self.open_folder_btn.configure(text=t.get("open_folder", "Abrir Pasta"))
        
        fmt_vals = [t["video_audio"], t["audio_only"], t["video_only"]]
        current_fmt_idx = 0
        try:
            current_fmt_idx = fmt_vals.index(self.type_var.get())
        except ValueError:
            current_fmt_idx = 1 if self.audio_only else 0
            
        self.type_menu.configure(values=fmt_vals)
        self.type_var.set(fmt_vals[current_fmt_idx])

        qual_vals = [t["best_quality"], "1080p", "720p", "480p", "360p"]
        current_qual_idx = 0
        try:
            current_qual_idx = qual_vals.index(self.quality_var.get())
        except ValueError:
            current_qual_idx = 0
            
        self.quality_menu.configure(values=qual_vals)
        self.quality_var.set(qual_vals[current_qual_idx])

    def update_progress(self, percent):
        self.progress_bar.set(percent)
        self.progress_label.configure(text=f"{int(percent * 100)}%")

    def start_download(self):
        url = self.url_entry.get().strip()
        
        # Extrair a URL limpa de textos compartilhados de aplicativos (ex: BiliBili)
        import re
        url_match = re.search(r'(https?://[^\s]+)', url)
        if url_match:
            url = url_match.group(1)
            
        lang = self.app_ref.config.get("language", "Português")
        t = LANGUAGES.get(lang, LANGUAGES["Português"])

        if not url:
            messagebox.showwarning("Aviso", t["empty_url"])
            return

        self.download_btn.configure(state="disabled")
        self.status_label.configure(text=t["downloading"], text_color="yellow")
        self.open_folder_btn.grid_remove()
        self.filename_label.grid_remove()
        
        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")
        self.progress_frame.grid()

        threading.Thread(target=self.download_media, args=(url, t), daemon=True).start()

    def open_download_folder(self):
        folder = self.app_ref.config.get("download_folder", "")
        if os.path.exists(folder):
            if os.name == 'nt':
                os.startfile(folder)
            else:
                import sys
                import subprocess
                if sys.platform == 'darwin':
                    subprocess.Popen(['open', folder])
                else:
                    subprocess.Popen(['xdg-open', folder])

    def download_media(self, url, t):
        try:
            original_url = url
            download_type = self.type_var.get()
            quality = self.quality_var.get()

            quality_str = ""
            if quality == "1080p":
                quality_str = "[height<=1080]"
            elif quality == "720p":
                quality_str = "[height<=720]"
            elif quality == "480p":
                quality_str = "[height<=480]"
            elif quality == "360p":
                quality_str = "[height<=360]"

            # Obter o executável do ffmpeg silenciosamente empacotado
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

            # ----- TRATAMENTO PARA LINKS DO SPOTIFY -----
            if "spotify" in url and "track" in url:
                self.status_label.configure(text=t["extracting"], text_color="yellow")
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    html = urllib.request.urlopen(req).read().decode('utf-8')
                    match = re.search(r'<title>(.*?)</title>', html)
                    if match:
                        full_title = match.group(1)
                        # Exemplo: "Never Gonna Give You Up - song and lyrics by Rick Astley | Spotify"
                        # Vamos limpar o título para facilitar a busca do yt-dlp
                        clean_title = full_title.replace(" | Spotify", "").replace("- song and lyrics by", "")
                        clean_title = clean_title.replace("- song by", "")
                        
                        self.status_label.configure(text=t["found"].format(clean_title), text_color="yellow")
                        # Transforma a URL num comando de busca para o YouTube, pra baixar a 1ª opção
                        url = f"ytsearch1:{clean_title}"
                    else:
                        raise Exception("Não foi possível encontrar o nome da música no link do Spotify.")
                except Exception as e:
                    raise Exception(f"Falha ao processar link do Spotify: {str(e)}")
            # --------------------------------------------

            download_folder = self.app_ref.config.get("download_folder", "")

            def progress_hook(d):
                if d['status'] == 'downloading':
                    try:
                        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
                        downloaded_bytes = d.get('downloaded_bytes', 0)
                        if total_bytes and total_bytes > 0:
                            percent = downloaded_bytes / total_bytes
                            self.app_ref.after(0, self.update_progress, percent)
                    except:
                        pass
                elif d['status'] == 'finished':
                    self.app_ref.after(0, self.update_progress, 1.0)

            ydl_opts = {
                'outtmpl': os.path.join(download_folder, f'%(title).70s - dummy.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'ffmpeg_location': ffmpeg_path,
                'postprocessors': [],
                'progress_hooks': [progress_hook],
                'windowsfilenames': True
            }

            if download_type == t["audio_only"] or self.audio_only:
                # Baixa a melhor fonte possível e converte para MP3 usando FFmpeg
                ydl_opts['format'] = 'bestaudio/best'
                sufixo_nome = "audio"
                ydl_opts['outtmpl'] = os.path.join(download_folder, f'%(title).70s - {sufixo_nome}.%(ext)s')
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                })
            elif download_type == t["video_only"]:
                # Força a baixar o formato unificado/melhor
                ydl_opts['format'] = f'bestvideo[ext=mp4]{quality_str}/best{quality_str}/best/bestvideo'
                sufixo_nome = f"vídeo - {quality}"
                ydl_opts['outtmpl'] = os.path.join(download_folder, f'%(title).70s - {sufixo_nome}.%(ext)s')
                # Remuxa para mp4 passando o argumento '-an' (No Audio) para remover a trilha sonora
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                })
                ydl_opts['postprocessor_args'] = ['-an']
            else:
                # Vídeo e Áudio combinados
                ydl_opts['format'] = f'bestvideo[ext=mp4]{quality_str}+bestaudio[ext=m4a]/best[ext=mp4]{quality_str}/best/bestvideo/bestaudio'
                sufixo_nome = f"video e audio - {quality}"
                ydl_opts['outtmpl'] = os.path.join(download_folder, f'%(title).70s - {sufixo_nome}.%(ext)s')
                # Se baixar as faixas separadas, o ffmpeg faz o merge automaticamente para o formato padrão do vídeo (mkv/mp4)
                # Vamos forçar que o resultado final sempre seja mp4 para compatibilidade Windows
                ydl_opts['merge_output_format'] = 'mp4'
                # Forçar a re-codificação de qualquer áudio bizarro (como Opus) para AAC, comum e suportado
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                })
                ydl_opts['postprocessor_args'] = ['-c:v', 'copy', '-c:a', 'aac']

            self.status_label.configure(text=t["downloading"], text_color="yellow")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
            title = "Arquivo Baixado"
            duration_str = ""
            if info:
                if 'entries' in info and len(info['entries']) > 0:
                    entry = info['entries'][0]
                    title = entry.get('title', 'Arquivo Baixado')
                    duration_sec = entry.get('duration', 0)
                else:
                    title = info.get('title', 'Arquivo Baixado')
                    duration_sec = info.get('duration', 0)
                    
                if duration_sec:
                    m, s = divmod(int(duration_sec), 60)
                    h, m = divmod(m, 60)
                    if h > 0:
                        duration_str = f"{h}:{m:02d}:{s:02d}"
                    else:
                        duration_str = f"{m}:{s:02d}"

            # Identificar o serviço pela URL original, antes de ser modificada pelo tratamento do Spotify
            service = "Desconhecido"
            url_lower_orig = original_url.lower()
            if "spotify" in url_lower_orig:
                service = "Spotify"
            elif "tiktok" in url_lower_orig:
                service = "TikTok"

            elif "instagram" in url_lower_orig:
                service = "Instagram"
            elif "twitter.com" in url_lower_orig or "x.com" in url_lower_orig:
                service = "Twitter"
            elif "reddit.com" in url_lower_orig:
                service = "Reddit"
            elif "pinterest." in url_lower_orig:
                service = "Pinterest"
            elif "facebook.com" in url_lower_orig or "fb.watch" in url_lower_orig:
                service = "Facebook"
            elif "kwai.com" in url_lower_orig:
                service = "Kwai"
            elif "vimeo.com" in url_lower_orig:
                service = "Vimeo"
            elif "twitch.tv" in url_lower_orig:
                service = "Twitch"
            elif "soundcloud.com" in url_lower_orig:
                service = "SoundCloud"
            elif "bandcamp.com" in url_lower_orig:
                service = "Bandcamp"
            elif "rumble.com" in url_lower_orig:
                service = "Rumble"
            elif "bilibili.tv" in url_lower_orig or "bilibili.com" in url_lower_orig:
                service = "BiliBili"
    
            elif "youtube" in url_lower_orig or "youtu.be" in url_lower_orig or "ytsearch1" in url_lower_orig:
                service = "YouTube"

            # Obter o caminho real do arquivo baixado
            final_path = ""
            if info and 'requested_downloads' in info and len(info['requested_downloads']) > 0:
                final_path = info['requested_downloads'][0].get('filepath', '')
            if not final_path and info and '_filename' in info:
                final_path = info['_filename']
            if not final_path:
                outtmpl = ydl_opts.get('outtmpl', '')
                if isinstance(outtmpl, dict):
                    outtmpl = outtmpl.get('default', '')
                if isinstance(outtmpl, str):
                    try:
                        final_path = outtmpl % {'title': title, 'ext': 'mp4'}
                    except:
                        final_path = os.path.join(download_folder, f"{title}.mp4")
                else:
                    final_path = os.path.join(download_folder, f"{title}.mp4")
            
            self.status_label.configure(text=t["done"], text_color="#00FF00")
            self.filename_label.configure(text=title)
            self.open_folder_btn.grid()
            self.filename_label.grid()
            
            # Adicionar ao histórico
            self.app_ref.add_to_history(title, service, duration_str, url, final_path)

            self.url_entry.delete(0, 'end')
            
        except Exception as e:
            error_msg = str(e)
            print(f"Erro no download: {error_msg}")
            self.status_label.configure(text=t["error_link"], text_color="red")
            messagebox.showerror("Download Erro", f"Ocorreu um erro ao baixar o arquivo.\n\nDetalhes do erro:\n{error_msg}")
        finally:
            self.download_btn.configure(state="normal")
            self.progress_frame.grid_remove()


class UniversalDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.load_config()
        
        # Carregar Tema (Padrão: system)
        theme = self.config.get("theme", "system")
        ctk.set_appearance_mode(theme)

        self.geometry("850x640")
        try:
            self.iconbitmap(os.path.join(os.path.dirname(__file__), "favIcon.ico"))
        except Exception:
            pass
        is_resizable = self.config.get("resizable_window", False)
        self.resizable(is_resizable, is_resizable)

        # Efeito de Blur removido conforme solicitado
        # Configuração do Fundo da Janela (#1c1c1c no modo escuro, #e0e0e0 no modo claro)
        self.configure(fg_color=BG_COLOR)

        # Configurar Grid principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkScrollableFrame(self, width=240, corner_radius=0, fg_color=SIDEBAR_COLOR)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        # Cabeçalho da Sidebar (Logo em texto grosso)
        try:
            logo_img_data = Image.open(os.path.join(os.path.dirname(__file__), "favIcon.ico")).resize((48, 48), Image.Resampling.LANCZOS)
            self.logo_image = ctk.CTkImage(light_image=logo_img_data, dark_image=logo_img_data, size=(48, 48))
            self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Paroni\nDownloader", image=self.logo_image, compound="top", font=ctk.CTkFont(size=16, weight="bold"), text_color=TEXT_COLOR, justify="center")
        except Exception:
            self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Paroni\nDownloader", font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_COLOR, justify="center")
            
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 20))

        self.SERVICES_INFO = {
            "youtube": {"emoji": "▷", "key": "youtube"},
            "spotify": {"emoji": "🎵", "key": "spotify"},
            "tiktok": {"emoji": "📱", "key": "tiktok"},
            "instagram": {"emoji": "📸", "key": "instagram"},
            "twitter": {"emoji": "🐦", "key": "twitter"},
            "reddit": {"emoji": "👽", "key": "reddit"},
            "pinterest": {"emoji": "📌", "key": "pinterest"},
            "facebook": {"emoji": "📘", "key": "facebook"},
            "kwai": {"emoji": "🔥", "key": "kwai"},
            "vimeo": {"emoji": "🎬", "key": "vimeo"},
            "twitch": {"emoji": "🟪", "key": "twitch"},
            "soundcloud": {"emoji": "☁️", "key": "soundcloud"},
            "bandcamp": {"emoji": "🎸", "key": "bandcamp"},
            "bilibili": {"emoji": "📺", "key": "bilibili"}
        }

        # Botões Dinâmicos da Sidebar
        self.shortcut_buttons = []
        for i in range(4):
            btn = self.create_sidebar_button("", i + 1, lambda idx=i: self.show_shortcut(idx))
            self.shortcut_buttons.append(btn)
            
        self.btn_others = self.create_sidebar_button("🌐 Todos os Serviços", 5, self.show_others)
        
        # Divider and Settings
        self.divider = ctk.CTkFrame(self.sidebar_frame, height=2, fg_color=ENTRY_BG)
        self.divider.grid(row=6, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.btn_history = self.create_sidebar_button("🕒 Histórico", 7, self.show_history)
        self.btn_settings = self.create_sidebar_button("⚙ Configurações", 8, self.show_settings)

        self.buttons = self.shortcut_buttons + [self.btn_others, self.btn_history, self.btn_settings]

        # Version label (visible but subtle)
        self.version_label = ctk.CTkLabel(self.sidebar_frame, text="", font=ctk.CTkFont(size=11), text_color="#5A5C66")
        self.version_label.grid(row=9, column=0, pady=(20, 10))

        # --- Frames (Páginas) ---
        self.youtube_frame = DownloaderFrame(self, self, "youtube", "placeholder_yt", audio_only=False)
        self.spotify_frame = DownloaderFrame(self, self, "spotify", "placeholder_sp", audio_only=True)
        self.tiktok_frame = DownloaderFrame(self, self, "tiktok", "placeholder_tk", audio_only=False)
        self.instagram_frame = DownloaderFrame(self, self, "instagram", "placeholder_ig", audio_only=False)
        self.others_frame = OthersFrame(self, self)
        
        self.twitter_frame = DownloaderFrame(self, self, "twitter", "placeholder_tw", audio_only=False)
        self.reddit_frame = DownloaderFrame(self, self, "reddit", "placeholder_re", audio_only=False)
        self.pinterest_frame = DownloaderFrame(self, self, "pinterest", "placeholder_pi", audio_only=False)
        self.facebook_frame = DownloaderFrame(self, self, "facebook", "placeholder_fa", audio_only=False)
        self.kwai_frame = DownloaderFrame(self, self, "kwai", "placeholder_kw", audio_only=False)
        self.vimeo_frame = DownloaderFrame(self, self, "vimeo", "placeholder_vi", audio_only=False)
        self.twitch_frame = DownloaderFrame(self, self, "twitch", "placeholder_tw", audio_only=False)
        self.soundcloud_frame = DownloaderFrame(self, self, "soundcloud", "placeholder_so", audio_only=True)
        self.bandcamp_frame = DownloaderFrame(self, self, "bandcamp", "placeholder_ba", audio_only=True)
        self.bilibili_frame = DownloaderFrame(self, self, "bilibili", "placeholder_bi", audio_only=False)

        self.history_frame = HistoryFrame(self, self)
        self.settings_frame = SettingsFrame(self, self)

        self.frames = [
            self.youtube_frame, self.spotify_frame, self.tiktok_frame, self.instagram_frame, self.others_frame,
            self.twitter_frame, self.reddit_frame, self.pinterest_frame, self.facebook_frame, self.kwai_frame, 
            self.vimeo_frame, self.twitch_frame, self.soundcloud_frame, self.bandcamp_frame, 
            self.bilibili_frame, self.history_frame, self.settings_frame
        ]
        
        self.frames_dict = {
            "youtube": self.youtube_frame, "spotify": self.spotify_frame,
            "tiktok": self.tiktok_frame, "instagram": self.instagram_frame,
            "twitter": self.twitter_frame, "reddit": self.reddit_frame,
            "pinterest": self.pinterest_frame, "facebook": self.facebook_frame,
            "kwai": self.kwai_frame, "vimeo": self.vimeo_frame,
            "twitch": self.twitch_frame, "soundcloud": self.soundcloud_frame,
            "bandcamp": self.bandcamp_frame, "bilibili": self.bilibili_frame
        }
    

        self.apply_translations(self.config.get("language", "Português"))
        self.update_sidebar_shortcuts()

        # Selecionar primeiro atalho por padrão
        if self.shortcut_buttons:
            self.show_shortcut(0)
        else:
            self.show_others()
            
        self.bind("<Configure>", self.check_menu_scroll)

    def check_menu_scroll(self, event):
        if event.widget == self:
            # The required height is roughly 640 for all menu items to be fully visible and have some padding
            if self.winfo_height() < 640:
                self.sidebar_frame._scrollbar.grid(row=1, column=1, sticky="nesw", pady=6)
            else:
                self.sidebar_frame._scrollbar.grid_forget()
                if hasattr(self.sidebar_frame, '_parent_canvas'):
                    self.sidebar_frame._parent_canvas.yview_moveto(0)

    def load_config(self):
        default_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'VIDEOS')
        if not os.path.exists(default_folder):
            os.makedirs(default_folder)
            
        self.config = {
            "download_folder": default_folder,
            "language": "Português",
            "theme": "system",
            "shortcuts": ["youtube", "spotify", "tiktok", "instagram"],
            "history": []
        }
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.config.update(data)
            except:
                pass

        # Intercept lang_setup.ini se existir (vindo do instalador)
        import sys
        if getattr(sys, 'frozen', False):
            lang_file = os.path.join(os.path.dirname(sys.executable), "lang_setup.ini")
        else:
            lang_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang_setup.ini")
            
        if os.path.exists(lang_file):
            try:
                import configparser
                parser = configparser.ConfigParser()
                parser.read(lang_file, encoding="utf-8")
                setup_lang = parser.get("Setup", "Language", fallback="").lower()
                lang_map = {
                    "brazilianportuguese": "Português",
                    "english": "English",
                    "spanish": "Español",
                    "russian": "Русский",
                    "japanese": "日本語",
                }
                if setup_lang in lang_map:
                    self.config["language"] = lang_map[setup_lang]
                    self.save_config()
                os.remove(lang_file)
            except:
                pass

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except:
            pass
            
    def apply_translations(self, lang):
        t = LANGUAGES.get(lang, LANGUAGES["Português"])
        # Title of main window
        self.title("Paroni Downloader")
        
        # Apply labels text logic (with emoji prefix maintained)
        self.update_sidebar_shortcuts()
        self.btn_others.configure(text="🌐 " + t.get("others", "Outros"))
        self.btn_history.configure(text="🕒 " + t.get("history", "Histórico"))
        self.btn_settings.configure(text="⚙ " + t["settings"])
        
        self.version_label.configure(text=f"{t['version']}: 1.5")
        
        for frame in [self.youtube_frame, self.spotify_frame, self.tiktok_frame, self.instagram_frame, self.others_frame,
                      self.twitter_frame, self.reddit_frame, self.pinterest_frame, self.facebook_frame, self.kwai_frame, 
                      self.vimeo_frame, self.twitch_frame, self.soundcloud_frame, self.bandcamp_frame, 
                      self.bilibili_frame, self.history_frame]:
            frame.translate_ui(lang)
    

    def update_sidebar_shortcuts(self):
        lang = self.config.get("language", "Português")
        t = LANGUAGES.get(lang, LANGUAGES["Português"])
        shortcuts = self.config.get("shortcuts", ["youtube", "spotify", "tiktok", "instagram"])
        
        for i in range(4):
            service_id = shortcuts[i] if i < len(shortcuts) else "others"
            info = self.SERVICES_INFO.get(service_id, self.SERVICES_INFO.get("others", {"emoji": "", "key": "others"}))
            
            trans_text = t.get(info["key"], service_id.capitalize())
            if " " in trans_text and "Baixador" in trans_text:
                trans_text = trans_text.split(" ")[-1]
                
            self.shortcut_buttons[i].configure(text=f"{info['emoji']} {trans_text}")

    def show_shortcut(self, idx):
        shortcuts = self.config.get("shortcuts", ["youtube", "spotify", "tiktok", "instagram"])
        service_id = shortcuts[idx] if idx < len(shortcuts) else "others"
        
        self.hide_all_frames()
        self.select_sidebar_button(self.shortcut_buttons[idx])
        
        frame = self.frames_dict.get(service_id, self.others_frame)
        frame.grid(row=0, column=1, sticky="nsew")

    def create_sidebar_button(self, text, row, command):
        btn = ctk.CTkButton(
            self.sidebar_frame, 
            text=text, 
            command=command,
            fg_color="transparent", 
            text_color=TEXT_COLOR, 
            hover_color="#121b2d",
            border_width=0,
            corner_radius=20,
            anchor="w",
            font=ctk.CTkFont(size=15, weight="normal"),
            height=40
        )
        btn.grid(row=row, column=0, padx=15, pady=8, sticky="ew")
        return btn

    def select_sidebar_button(self, btn_ref):
        # Deselect all
        for btn in self.buttons:
            btn.configure(fg_color="transparent", border_width=0)
        # Select active
        btn_ref.configure(fg_color=ACCENT_COLOR, border_width=0)

    def hide_all_frames(self):
        for frame in self.frames:
            frame.grid_forget()

    def show_service(self, service_id):
        self.hide_all_frames()
        shortcuts = self.config.get("shortcuts", ["youtube", "spotify", "tiktok", "instagram"])
        if service_id in shortcuts:
            idx = shortcuts.index(service_id)
            self.select_sidebar_button(self.shortcut_buttons[idx])
        else:
            self.select_sidebar_button(self.btn_others)
        
        frame = self.frames_dict.get(service_id, self.others_frame)
        frame.grid(row=0, column=1, sticky="nsew")

    def show_youtube(self):
        self.show_service("youtube")

    def show_spotify(self):
        self.show_service("spotify")

    def show_tiktok(self):
        self.show_service("tiktok")

    def show_instagram(self):
        self.show_service("instagram")

    def show_others(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_others)
        self.others_frame.grid(row=0, column=1, sticky="nsew")

    def show_twitter(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_others)  # Mantém o menu lateral selecionado
        self.twitter_frame.grid(row=0, column=1, sticky="nsew")
        
    def show_reddit(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_others)
        self.reddit_frame.grid(row=0, column=1, sticky="nsew")
        
    def show_pinterest(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_others)
        self.pinterest_frame.grid(row=0, column=1, sticky="nsew")
        
    def show_facebook(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_others)
        self.facebook_frame.grid(row=0, column=1, sticky="nsew")
        
    def show_kwai(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_others)
        self.kwai_frame.grid(row=0, column=1, sticky="nsew")
        
    def show_vimeo(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_others)
        self.vimeo_frame.grid(row=0, column=1, sticky="nsew")
        
    def show_twitch(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_others)
        self.twitch_frame.grid(row=0, column=1, sticky="nsew")
        
    def show_soundcloud(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_others)
        self.soundcloud_frame.grid(row=0, column=1, sticky="nsew")
        
    def show_bandcamp(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_others)
        self.bandcamp_frame.grid(row=0, column=1, sticky="nsew")
        
    def show_bilibili(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_others)
        self.bilibili_frame.grid(row=0, column=1, sticky="nsew")

    def show_history(self):
    
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_history)
        self.history_frame.grid(row=0, column=1, sticky="nsew")

    def show_settings(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_settings)
        self.settings_frame.grid(row=0, column=1, sticky="nsew")

    def add_to_history(self, media_name, service, duration, link, path):
        entry = {
            "name": media_name,
            "service": service,
            "duration": duration,
            "link": link,
            "path": path
        }
        if "history" not in self.config:
            self.config["history"] = []
        
        # Add to the beginning of the list to keep it recent first
        self.config["history"].insert(0, entry)
        
        # Keep only the last 50 items to prevent the file from growing too large
        if len(self.config["history"]) > 50:
            self.config["history"] = self.config["history"][:50]
            
        self.save_config()
        
        # Update UI thread-safely
        self.after(0, lambda: self.history_frame.load_history(self.config["history"]))


if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = UniversalDownloaderApp()
    app.mainloop()
