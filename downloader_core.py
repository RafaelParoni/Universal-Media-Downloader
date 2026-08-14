import os
import re
import json
import urllib.request
import urllib.error
import threading
import uuid
import time
import base64
import io

try:
    import yt_dlp
    import imageio_ffmpeg
except ImportError:
    import sys
    import subprocess
    if not getattr(sys, 'frozen', False):
        print("Installing required packages (yt-dlp, imageio-ffmpeg)...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp", "imageio-ffmpeg"])
    import yt_dlp
    import imageio_ffmpeg

try:
    from service_icons import ICONS_B64
except ImportError:
    ICONS_B64 = {}

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
        "placeholder_pi": "在此粘贴Pinterest Pin链接...",
        "placeholder_fa": "在此粘贴Facebook视频链接...",
        "placeholder_kw": "在此粘贴Kwai视频链接...",
        "placeholder_vi": "在此粘贴Vimeo视频链接...",
        "placeholder_tw": "在此粘贴Twitch剪辑/VOD链接...",
        "placeholder_so": "在此粘贴SoundCloud歌曲链接... (仅音频)",
        "placeholder_ba": "在此粘贴Bandcamp歌曲链接... (仅音频)",
        "placeholder_ru": "在此粘贴Rumble视频链接...",
        "placeholder_bi": "在此粘贴BiliBili视频链接...",
        "btn_download": "下载",
        "video_audio": "视频 + 音频",
        "audio_only": "仅音频",
        "video_only": "仅视频",
        "best_quality": "最佳画质",
        "select_folder": "选择下载文件夹",
        "language_lbl": "应用语言:",
        "save_settings": "保存设置",
        "empty_url": "请输入有效的链接。",
        "downloading": "下载中... (根据网络情况可能需要一点时间)",
        "done": "下载完成！已保存至指定文件夹。",
        "extracting": "正在提取Spotify信息...",
        "found": "已找到: {}。正在搜索音频...",
        "error_link": "错误: 请检查链接或网络连接。",
        "open_folder": "打开文件夹",
        "version": "版本",
        "history": "历史记录",
        "media_name": "媒体名称",
        "service": "服务",
        "duration": "时长",
        "link": "链接",
        "location": "位置",
        "no_history": "暂无历史记录。",
        "delete": "删除"
    }
}

SERVICES_METADATA = [
    {"id": "youtube", "name": "YouTube", "video": True, "audio": True, "placeholder": "placeholder_yt"},
    {"id": "spotify", "name": "Spotify", "video": False, "audio": True, "placeholder": "placeholder_sp"},
    {"id": "tiktok", "name": "TikTok", "video": True, "audio": True, "placeholder": "placeholder_tk"},
    {"id": "instagram", "name": "Instagram", "video": True, "audio": True, "placeholder": "placeholder_ig"},
    {"id": "twitter", "name": "Twitter (X)", "video": True, "audio": True, "placeholder": "placeholder_tw"},
    {"id": "reddit", "name": "Reddit", "video": True, "audio": True, "placeholder": "placeholder_re"},
    {"id": "pinterest", "name": "Pinterest", "video": True, "audio": True, "placeholder": "placeholder_pi"},
    {"id": "facebook", "name": "Facebook", "video": True, "audio": True, "placeholder": "placeholder_fa"},
    {"id": "kwai", "name": "Kwai", "video": True, "audio": True, "placeholder": "placeholder_kw"},
    {"id": "vimeo", "name": "Vimeo", "video": True, "audio": True, "placeholder": "placeholder_vi"},
    {"id": "twitch", "name": "Twitch", "video": True, "audio": True, "placeholder": "placeholder_tw"},
    {"id": "soundcloud", "name": "SoundCloud", "video": False, "audio": True, "placeholder": "placeholder_so"},
    {"id": "bandcamp", "name": "Bandcamp", "video": False, "audio": True, "placeholder": "placeholder_ba"},
    {"id": "bilibili", "name": "BiliBili", "video": True, "audio": True, "placeholder": "placeholder_bi"}
]

class ConfigManager:
    """Manages application configurations and download history."""
    
    @staticmethod
    def get_default_download_folder():
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

    @classmethod
    def load_config(cls):
        default_config = {
            "download_folder": cls.get_default_download_folder(),
            "language": "Português",
            "theme": "system",
            "shortcuts": ["youtube", "spotify", "tiktok", "instagram"],
            "history": [],
            "resizable_window": True,
            "master_pin": "",
            "port": 3000,
            "bind_address": "0.0.0.0"
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    default_config.update(config)
            except Exception as e:
                print(f"Error loading config file: {e}")
        
        # Verify configured folder exists, otherwise fallback to project temp folder
        folder = default_config.get("download_folder", "")
        if not folder or not os.path.exists(folder):
            default_config["download_folder"] = cls.get_default_download_folder()

        return default_config

    @classmethod
    def save_config(cls, config_data):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config file: {e}")
            return False

    @classmethod
    def add_to_history(cls, name, service, duration, link, file_path):
        config = cls.load_config()
        history = config.get("history", [])
        entry = {
            "name": name,
            "service": service,
            "duration": duration,
            "link": link,
            "path": file_path,
            "timestamp": time.time()
        }
        # Avoid exact duplicate links at top
        history = [h for h in history if h.get("link") != link or h.get("path") != file_path]
        history.append(entry)
        config["history"] = history
        cls.save_config(config)
        return entry

    @classmethod
    def delete_history_item(cls, link_or_path):
        config = cls.load_config()
        history = config.get("history", [])
        new_history = [h for h in history if h.get("link") != link_or_path and h.get("path") != link_or_path]
        config["history"] = new_history
        cls.save_config(config)
        return new_history


class DownloadJob:
    """Represents a download job state."""
    def __init__(self, job_id, url, download_type="video_audio", quality="best_quality"):
        self.job_id = job_id
        self.url = url
        self.download_type = download_type
        self.quality = quality
        self.status = "queued"  # queued, downloading, processing, finished, error
        self.progress = 0.0     # 0.0 to 1.0
        self.status_message = ""
        self.filename = ""
        self.final_path = ""
        self.service = "Desconhecido"
        self.duration = ""
        self.error_message = ""
        self.start_time = time.time()

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "url": self.url,
            "download_type": self.download_type,
            "quality": self.quality,
            "status": self.status,
            "progress": round(self.progress, 3),
            "status_message": self.status_message,
            "filename": self.filename,
            "final_path": self.final_path,
            "service": self.service,
            "duration": self.duration,
            "error_message": self.error_message
        }


class MediaDownloaderEngine:
    """Core downloading engine extracted from GUI."""
    
    def __init__(self):
        self.jobs = {}
        self.lock = threading.Lock()

    def create_job(self, url, download_type="video_audio", quality="best_quality"):
        job_id = str(uuid.uuid4())
        job = DownloadJob(job_id, url, download_type, quality)
        with self.lock:
            self.jobs[job_id] = job
        
        # Start download thread
        thread = threading.Thread(target=self._run_download, args=(job,), daemon=True)
        thread.start()
        return job_id

    def get_job(self, job_id):
        with self.lock:
            return self.jobs.get(job_id)

    def _detect_service(self, original_url):
        url_lower = original_url.lower()
        if "spotify" in url_lower:
            return "Spotify"
        elif "tiktok" in url_lower:
            return "TikTok"
        elif "instagram" in url_lower:
            return "Instagram"
        elif "twitter.com" in url_lower or "x.com" in url_lower:
            return "Twitter"
        elif "reddit.com" in url_lower:
            return "Reddit"
        elif "pinterest." in url_lower:
            return "Pinterest"
        elif "facebook.com" in url_lower or "fb.watch" in url_lower:
            return "Facebook"
        elif "kwai.com" in url_lower:
            return "Kwai"
        elif "vimeo.com" in url_lower:
            return "Vimeo"
        elif "twitch.tv" in url_lower:
            return "Twitch"
        elif "soundcloud.com" in url_lower:
            return "SoundCloud"
        elif "bandcamp.com" in url_lower:
            return "Bandcamp"
        elif "rumble.com" in url_lower:
            return "Rumble"
        elif "bilibili.tv" in url_lower or "bilibili.com" in url_lower:
            return "BiliBili"
        elif "youtube" in url_lower or "youtu.be" in url_lower or "ytsearch1" in url_lower:
            return "YouTube"
        return "Desconhecido"

    def _run_download(self, job):
        config = ConfigManager.load_config()
        lang = config.get("language", "Português")
        t = LANGUAGES.get(lang, LANGUAGES["Português"])

        url = job.url.strip()
        # Extract clean URL from shared texts (e.g., BiliBili share links)
        url_match = re.search(r'(https?://[^\s]+)', url)
        if url_match:
            url = url_match.group(1)

        original_url = url
        job.service = self._detect_service(original_url)

        if not url:
            job.status = "error"
            job.error_message = t.get("empty_url", "URL inválida.")
            job.status_message = job.error_message
            return

        job.status = "downloading"
        job.status_message = t.get("downloading", "Baixando...")

        try:
            quality_str = ""
            if job.quality == "1080p":
                quality_str = "[height<=1080]"
            elif job.quality == "720p":
                quality_str = "[height<=720]"
            elif job.quality == "480p":
                quality_str = "[height<=480]"
            elif job.quality == "360p":
                quality_str = "[height<=360]"

            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

            # Spotify link handling
            if "spotify" in url and "track" in url:
                job.status_message = t.get("extracting", "Extraindo informações do Spotify...")
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    html = urllib.request.urlopen(req).read().decode('utf-8')
                    match = re.search(r'<title>(.*?)</title>', html)
                    if match:
                        full_title = match.group(1)
                        clean_title = full_title.replace(" | Spotify", "").replace("- song and lyrics by", "").replace("- song by", "")
                        job.status_message = t.get("found", "Encontrado: {}").format(clean_title)
                        url = f"ytsearch1:{clean_title}"
                    else:
                        raise Exception("Não foi possível encontrar o nome da música no link do Spotify.")
                except Exception as e:
                    raise Exception(f"Falha ao processar link do Spotify: {str(e)}")

            TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
            if not os.path.exists(TEMP_DIR):
                os.makedirs(TEMP_DIR, exist_ok=True)
            download_folder = TEMP_DIR

            def progress_hook(d):
                if d['status'] == 'downloading':
                    try:
                        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
                        downloaded_bytes = d.get('downloaded_bytes', 0)
                        if total_bytes and total_bytes > 0:
                            job.progress = min(0.95, downloaded_bytes / total_bytes)
                    except Exception:
                        pass
                elif d['status'] == 'finished':
                    job.progress = 0.99
                    job.status = "processing"
                    job.status_message = "Processando arquivo..."

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

            # Format options
            dtype = job.download_type
            if dtype == "audio_only" or dtype == t.get("audio_only") or dtype == "Apenas Áudio" or dtype == "Audio Only":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['outtmpl'] = os.path.join(download_folder, f'%(title).70s - audio.%(ext)s')
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                })
            elif dtype == "video_only" or dtype == t.get("video_only") or dtype == "Apenas Vídeo" or dtype == "Video Only":
                ydl_opts['format'] = f'bestvideo[ext=mp4]{quality_str}/best{quality_str}/best/bestvideo'
                ydl_opts['outtmpl'] = os.path.join(download_folder, f'%(title).70s - vídeo - {job.quality}.%(ext)s')
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                })
                ydl_opts['postprocessor_args'] = ['-an']
            else: # video_audio
                ydl_opts['format'] = f'bestvideo[ext=mp4]{quality_str}+bestaudio[ext=m4a]/best[ext=mp4]{quality_str}/best/bestvideo/bestaudio'
                ydl_opts['outtmpl'] = os.path.join(download_folder, f'%(title).70s - video e audio - {job.quality}.%(ext)s')
                ydl_opts['merge_output_format'] = 'mp4'
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                })
                ydl_opts['postprocessor_args'] = ['-c:v', 'copy', '-c:a', 'aac']

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
                    duration_str = f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m}:{s:02d}"

            final_path = ""
            if info and 'requested_downloads' in info and len(info['requested_downloads']) > 0:
                final_path = info['requested_downloads'][0].get('filepath', '')
            if not final_path and info and '_filename' in info:
                final_path = info['_filename']
            if not final_path:
                final_path = os.path.join(download_folder, f"{title}.mp4")

            job.filename = title
            job.final_path = final_path
            job.duration = duration_str
            job.progress = 1.0
            job.status = "finished"
            job.status_message = t.get("done", "Download concluído!")

            # Add to history
            ConfigManager.add_to_history(title, job.service, duration_str, original_url, final_path)

            # Schedule file deletion after 5 minutes (300 seconds)
            self._schedule_file_deletion(final_path, delay_seconds=300)

        except Exception as e:
            error_msg = str(e)
            print(f"[Engine] Download Error: {error_msg}")
            job.status = "error"
            job.error_message = error_msg
            job.status_message = t.get("error_link", "Erro no download.")

    def _schedule_file_deletion(self, file_path, delay_seconds=300):
        def _cleanup():
            time.sleep(delay_seconds)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"[Cleanup] Deleted temporary file after 5min: {file_path}")
            except Exception as e:
                print(f"[Cleanup Error] {e}")

        threading.Thread(target=_cleanup, daemon=True).start()

# Global engine instance
engine_instance = MediaDownloaderEngine()
