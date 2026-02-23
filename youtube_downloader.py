import os
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
import urllib.request
import urllib.error
import re
import json

try:
    import customtkinter as ctk
    import yt_dlp
    import imageio_ffmpeg
except ImportError:
    import sys
    import subprocess
    print("Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter", "yt-dlp", "imageio-ffmpeg"])
    import customtkinter as ctk
    import yt_dlp
    import imageio_ffmpeg

# Paleta de Cores (Mockup)
BG_COLOR = "#0A0B10"           # Fundo muito escuro (Janela principal)
SIDEBAR_COLOR = "#0F111A"      # Fundo da barra lateral
CARD_COLOR = "#151720"         # Fundo dos "cards" arredondados centrais
ACCENT_COLOR = "#6C5CE7"       # Roxo Vibrante
ACCENT_HOVER = "#5848C2"       # Roxo mais escuro
ENTRY_BG = "#222433"           # Fundo das caixas de texto
TEXT_COLOR = "#FFFFFF"         # Texto claro

# Configuração Base
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "config.json"

LANGUAGES = {
    "Português": {
        "title": "Universal Media Downloader",
        "youtube": "Baixador do YouTube",
        "spotify": "Baixador do Spotify",
        "tiktok": "Baixador do TikTok",
        "instagram": "Baixador do Instagram",
        "settings": "Configurações",
        "placeholder_yt": "Cole o link do vídeo do YouTube...",
        "placeholder_sp": "Cole o link da música do Spotify... (Apenas Áudio)",
        "placeholder_tk": "Cole o link do vídeo do TikTok...",
        "placeholder_ig": "Cole o link do Reels/Post do Instagram...",
        "btn_download": "Baixar",
        "video_audio": "Vídeo + Áudio",
        "audio_only": "Apenas Áudio",
        "video_only": "Apenas Vídeo",
        "best_quality": "Melhor Qualidade",
        "select_folder": "Escolher Pasta de Download",
        "language_lbl": "Idioma do Aplicativo:",
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
        "title": "Universal Media Downloader",
        "youtube": "YouTube Downloader",
        "spotify": "Spotify Downloader",
        "tiktok": "TikTok Downloader",
        "instagram": "Instagram Downloader",
        "settings": "Settings",
        "placeholder_yt": "Paste YouTube video link here...",
        "placeholder_sp": "Paste Spotify track link here... (Audio Only)",
        "placeholder_tk": "Paste TikTok video link here...",
        "placeholder_ig": "Paste Instagram Reels/Post link here...",
        "btn_download": "Download",
        "video_audio": "Video + Audio",
        "audio_only": "Audio Only",
        "video_only": "Video Only",
        "best_quality": "Best Quality",
        "select_folder": "Choose Download Folder",
        "language_lbl": "App Language:",
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
        "title": "Universal Media Downloader",
        "youtube": "Descargador de YouTube",
        "spotify": "Descargador de Spotify",
        "tiktok": "Descargador de TikTok",
        "instagram": "Descargador de Instagram",
        "settings": "Ajustes",
        "placeholder_yt": "Pega el enlace del video de YouTube aquí...",
        "placeholder_sp": "Pega el enlace de la pista de Spotify... (Solo Audio)",
        "placeholder_tk": "Pega el enlace del video de TikTok aquí...",
        "placeholder_ig": "Pega el enlace de Reels/Post de Instagram...",
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
        "title": "Universal Media Downloader",
        "youtube": "Загрузчик YouTube",
        "spotify": "Загрузчик Spotify",
        "tiktok": "Загрузчик TikTok",
        "instagram": "Загрузчик Instagram",
        "settings": "Настройки",
        "placeholder_yt": "Вставьте ссылку на видео YouTube...",
        "placeholder_sp": "Вставьте ссылку на трек Spotify... (Только аудио)",
        "placeholder_tk": "Вставьте ссылку на видео TikTok...",
        "placeholder_ig": "Вставьте ссылку на Reels/Post Instagram...",
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
        "title": "Universal Media Downloader",
        "youtube": "YouTube ダウンローダー",
        "spotify": "Spotify ダウンローダー",
        "tiktok": "TikTok ダウンローダー",
        "instagram": "Instagram ダウンローダー",
        "settings": "設定",
        "placeholder_yt": "YouTubeの動画リンクを貼り付け...",
        "placeholder_sp": "Spotifyのリンクを貼り付け... (音声のみ)",
        "placeholder_tk": "TikTokの動画リンクを貼り付け...",
        "placeholder_ig": "InstagramのReels/Postリンクを貼り付け...",
        "btn_download": "ダウンロード",
        "video_audio": "ビデオ + 音声",
        "audio_only": "音声のみ",
        "video_only": "ビデオのみ",
        "best_quality": "最高画質",
        "select_folder": "保存先フォルダを選択",
        "language_lbl": "アプリの言語:",
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
        "title": "Universal Media Downloader",
        "youtube": "YouTube 下载器",
        "spotify": "Spotify 下载器",
        "tiktok": "TikTok 下载器",
        "instagram": "Instagram 下载器",
        "settings": "设置",
        "placeholder_yt": "在此粘贴YouTube视频链接...",
        "placeholder_sp": "在此粘贴Spotify歌曲链接... (仅音频)",
        "placeholder_tk": "在此粘贴TikTok视频链接...",
        "placeholder_ig": "在此粘贴Instagram Reels/Post链接...",
        "btn_download": "下载",
        "video_audio": "视频 + 音频",
        "audio_only": "仅音频",
        "video_only": "仅视频",
        "best_quality": "最佳质量",
        "select_folder": "选择下载文件夹",
        "language_lbl": "应用语言:",
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

class HistoryFrame(ctk.CTkFrame):
    def __init__(self, master, app_ref):
        super().__init__(master, corner_radius=0, fg_color=BG_COLOR)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.app_ref = app_ref

        # Card Central
        self.card = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=25)
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
        
        item_frame = ctk.CTkFrame(self.scroll_frame, fg_color=ENTRY_BG, corner_radius=15)
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


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, app_ref):
        # Atualização Visual
        super().__init__(master, corner_radius=0, fg_color=BG_COLOR)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.app_ref = app_ref

        # Card Central
        self.card = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=25)
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
        self.menu_lang.grid(row=4, column=0, pady=(0, 30))

        # Save button
        self.btn_save = ctk.CTkButton(
            self.card, text="Salvar Configurações", 
            command=self.save_settings, font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER, corner_radius=20, height=45, width=220
        )
        self.btn_save.grid(row=5, column=0, pady=(20, 10))
        
        self.status_label = ctk.CTkLabel(self.card, text="", font=ctk.CTkFont(size=13))
        self.status_label.grid(row=6, column=0, pady=(0, 20))

        self.translate_ui(self.lang_var.get())

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)
            
    def change_language(self, new_lang):
        self.translate_ui(new_lang)
        self.app_ref.apply_translations(new_lang)

    def translate_ui(self, lang):
        t = LANGUAGES.get(lang, LANGUAGES["Português"])
        self.title_label.configure(text=t["settings"])
        self.btn_folder.configure(text=t["select_folder"])
        self.lbl_lang.configure(text=t["language_lbl"])
        self.btn_save.configure(text=t["save_settings"])

    def save_settings(self):
        self.app_ref.config["download_folder"] = self.folder_var.get()
        self.app_ref.config["language"] = self.lang_var.get()
        self.app_ref.save_config()
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
        self.card = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=25)
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
            border_color=ACCENT_COLOR,
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

        # Botão de Download Moderno e Largo
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

        self.status_label = ctk.CTkLabel(self.card, text="", font=ctk.CTkFont(size=13))
        self.status_label.grid(row=4, column=0, pady=(0, 10))

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
        self.open_folder_btn.grid(row=5, column=0, pady=(0, 10))
        self.open_folder_btn.grid_remove()

        self.filename_label = ctk.CTkLabel(self.card, text="", font=ctk.CTkFont(size=14, weight="bold"), text_color="#AAAAAA", wraplength=400)
        self.filename_label.grid(row=6, column=0, pady=(0, 20))
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

    def start_download(self):
        url = self.url_entry.get().strip()
        lang = self.app_ref.config.get("language", "Português")
        t = LANGUAGES.get(lang, LANGUAGES["Português"])

        if not url:
            messagebox.showwarning("Aviso", t["empty_url"])
            return

        self.download_btn.configure(state="disabled")
        self.status_label.configure(text=t["downloading"], text_color="yellow")
        self.open_folder_btn.grid_remove()
        self.filename_label.grid_remove()

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

            ydl_opts = {
                'outtmpl': os.path.join(download_folder, f'%(title)s - dummy.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'ffmpeg_location': ffmpeg_path,
                'postprocessors': []
            }

            if download_type == t["audio_only"] or self.audio_only:
                # Baixa a melhor fonte possível e converte para MP3 usando FFmpeg
                ydl_opts['format'] = 'bestaudio/best'
                sufixo_nome = "audio"
                ydl_opts['outtmpl'] = os.path.join(download_folder, f'%(title)s - {sufixo_nome}.%(ext)s')
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                })
            elif download_type == t["video_only"]:
                # Força a baixar o formato unificado/melhor
                ydl_opts['format'] = f'bestvideo[ext=mp4]{quality_str}/best{quality_str}/best'
                sufixo_nome = f"vídeo - {quality}"
                ydl_opts['outtmpl'] = os.path.join(download_folder, f'%(title)s - {sufixo_nome}.%(ext)s')
                # Remuxa para mp4 passando o argumento '-an' (No Audio) para remover a trilha sonora
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                })
                ydl_opts['postprocessor_args'] = ['-an']
            else:
                # Vídeo e Áudio combinados
                ydl_opts['format'] = f'bestvideo[ext=mp4]{quality_str}+bestaudio[ext=m4a]/best[ext=mp4]{quality_str}/best'
                sufixo_nome = f"video e audio - {quality}"
                ydl_opts['outtmpl'] = os.path.join(download_folder, f'%(title)s - {sufixo_nome}.%(ext)s')
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


class UniversalDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.load_config()

        self.geometry("850x500")
        self.resizable(False, False)

        # Configurar Grid principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=SIDEBAR_COLOR)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        # Cabeçalho da Sidebar (Logo em texto grosso)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Universal Media\nDownloader", font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_COLOR, justify="center")
        self.logo_label.grid(row=0, column=0, padx=10, pady=(30, 30))

        # Botões do Sidebar (Nomes + Emojis)
        self.btn_youtube = self.create_sidebar_button("▷ YouTube", 1, self.show_youtube)
        self.btn_spotify = self.create_sidebar_button("🎵 Spotify", 2, self.show_spotify)
        self.btn_tiktok = self.create_sidebar_button("📱 TikTok", 3, self.show_tiktok)
        self.btn_instagram = self.create_sidebar_button("📸 Instagram", 4, self.show_instagram)
        
        # Divider and Settings
        self.divider = ctk.CTkFrame(self.sidebar_frame, height=2, fg_color=ENTRY_BG)
        self.divider.grid(row=5, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.btn_history = self.create_sidebar_button("🕒 Histórico", 6, self.show_history)
        self.btn_settings = self.create_sidebar_button("⚙ Configurações", 7, self.show_settings)

        self.buttons = [self.btn_youtube, self.btn_spotify, self.btn_tiktok, self.btn_instagram, self.btn_history, self.btn_settings]

        # Version label (visible but subtle)
        self.version_label = ctk.CTkLabel(self.sidebar_frame, text="", font=ctk.CTkFont(size=11), text_color="#5A5C66")
        self.version_label.grid(row=8, column=0, pady=(0, 10), sticky="s")

        # --- Frames (Páginas) ---
        self.youtube_frame = DownloaderFrame(self, self, "youtube", "placeholder_yt", audio_only=False)
        self.spotify_frame = DownloaderFrame(self, self, "spotify", "placeholder_sp", audio_only=True)
        self.tiktok_frame = DownloaderFrame(self, self, "tiktok", "placeholder_tk", audio_only=False)
        self.instagram_frame = DownloaderFrame(self, self, "instagram", "placeholder_ig", audio_only=False)
        self.history_frame = HistoryFrame(self, self)
        self.settings_frame = SettingsFrame(self, self)

        self.frames = [self.youtube_frame, self.spotify_frame, self.tiktok_frame, self.instagram_frame, self.history_frame, self.settings_frame]

        self.apply_translations(self.config.get("language", "Português"))

        # Selecionar YouTube por padrão
        self.show_youtube()

    def load_config(self):
        default_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'VIDEOS')
        if not os.path.exists(default_folder):
            os.makedirs(default_folder)
            
        self.config = {
            "download_folder": default_folder,
            "language": "Português",
            "history": []
        }
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.config.update(data)
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
        self.title("Universal Media Downloader")
        
        # Apply labels text logic (with emoji prefix maintained)
        self.btn_youtube.configure(text="▷ " + t["youtube"].split(" ")[-1]) 
        self.btn_spotify.configure(text="🎵 " + t["spotify"].split(" ")[-1])
        self.btn_tiktok.configure(text="📱 " + t["tiktok"].split(" ")[-1])
        self.btn_instagram.configure(text="📸 " + t["instagram"].split(" ")[-1])
        self.btn_history.configure(text="🕒 " + t.get("history", "Histórico"))
        self.btn_settings.configure(text="⚙ " + t["settings"])
        
        self.version_label.configure(text=f"{t['version']}: 1.2.2")
        
        for frame in [self.youtube_frame, self.spotify_frame, self.tiktok_frame, self.instagram_frame, self.history_frame]:
            frame.translate_ui(lang)

    def create_sidebar_button(self, text, row, command):
        btn = ctk.CTkButton(
            self.sidebar_frame, 
            text=text, 
            command=command,
            fg_color="transparent", 
            text_color=TEXT_COLOR, 
            hover_color=CARD_COLOR,
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
            btn.configure(fg_color="transparent")
        # Select active
        btn_ref.configure(fg_color=ACCENT_COLOR)

    def hide_all_frames(self):
        for frame in self.frames:
            frame.grid_forget()

    def show_youtube(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_youtube)
        self.youtube_frame.grid(row=0, column=1, sticky="nsew")

    def show_spotify(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_spotify)
        self.spotify_frame.grid(row=0, column=1, sticky="nsew")

    def show_tiktok(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_tiktok)
        self.tiktok_frame.grid(row=0, column=1, sticky="nsew")

    def show_instagram(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_instagram)
        self.instagram_frame.grid(row=0, column=1, sticky="nsew")

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
    app = UniversalDownloaderApp()
    app.mainloop()
