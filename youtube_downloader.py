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
    }
}

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
        self.status_label.grid(row=4, column=0, pady=(0, 20))

        self.translate_ui(self.app_ref.config.get("language", "Português"))

    def translate_ui(self, lang):
        t = LANGUAGES.get(lang, LANGUAGES["Português"])
        
        self.title_label.configure(text=t[self.title_key])
        self.url_entry.configure(placeholder_text=t[self.placeholder_key])
        self.download_btn.configure(text=t["btn_download"])
        
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
        threading.Thread(target=self.download_media, args=(url, t), daemon=True).start()

    def download_media(self, url, t):
        try:
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
                ydl.download([url])

            self.status_label.configure(text=t["done"], text_color="#00FF00")
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
        
        self.btn_settings = self.create_sidebar_button("⚙ Configurações", 6, self.show_settings)

        self.buttons = [self.btn_youtube, self.btn_spotify, self.btn_tiktok, self.btn_instagram, self.btn_settings]

        # --- Frames (Páginas) ---
        self.youtube_frame = DownloaderFrame(self, self, "youtube", "placeholder_yt", audio_only=False)
        self.spotify_frame = DownloaderFrame(self, self, "spotify", "placeholder_sp", audio_only=True)
        self.tiktok_frame = DownloaderFrame(self, self, "tiktok", "placeholder_tk", audio_only=False)
        self.instagram_frame = DownloaderFrame(self, self, "instagram", "placeholder_ig", audio_only=False)
        self.settings_frame = SettingsFrame(self, self)

        self.frames = [self.youtube_frame, self.spotify_frame, self.tiktok_frame, self.instagram_frame, self.settings_frame]

        self.apply_translations(self.config.get("language", "Português"))

        # Selecionar YouTube por padrão
        self.show_youtube()

    def load_config(self):
        default_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'VIDEOS')
        if not os.path.exists(default_folder):
            os.makedirs(default_folder)
            
        self.config = {
            "download_folder": default_folder,
            "language": "Português"
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
        self.btn_settings.configure(text="⚙ " + t["settings"])
        
        for frame in [self.youtube_frame, self.spotify_frame, self.tiktok_frame, self.instagram_frame]:
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

    def show_settings(self):
        self.hide_all_frames()
        self.select_sidebar_button(self.btn_settings)
        self.settings_frame.grid(row=0, column=1, sticky="nsew")


if __name__ == "__main__":
    app = UniversalDownloaderApp()
    app.mainloop()
