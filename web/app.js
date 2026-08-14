// Paroni Downloader Web Client Application
let currentConfig = {};
let availableServices = [];
let activeService = "youtube";
let activeJobId = null;
let pollTimer = null;

const LANGUAGES = {
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
        "settings": "Configurações",
        "history": "Histórico",
        "btn_download": "Baixar",
        "video_audio": "Vídeo + Áudio",
        "audio_only": "Apenas Áudio",
        "video_only": "Apenas Vídeo",
        "best_quality": "Melhor Qualidade",
        "select_folder": "Pasta de Download no Servidor",
        "language_lbl": "Idioma da Interface",
        "save_settings": "Salvar Configurações",
        "empty_url": "Por favor, insira um link válido.",
        "downloading": "Baixando...",
        "done": "Download concluído!",
        "open_folder": "Baixar no Navegador",
        "no_history": "Nenhum histórico disponível.",
        "delete": "Excluir",
        "format": "Formato",
        "quality": "Qualidade",
        "shortcuts": "Atalhos",
        "all_services_title": "Todos os Serviços Suportados",
        "clear_all": "Limpar Tudo",
        "saved_success": "Configurações salvas com sucesso!"
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
        "settings": "Settings",
        "history": "History",
        "btn_download": "Download",
        "video_audio": "Video + Audio",
        "audio_only": "Audio Only",
        "video_only": "Video Only",
        "best_quality": "Best Quality",
        "select_folder": "Server Download Folder",
        "language_lbl": "Interface Language",
        "save_settings": "Save Settings",
        "empty_url": "Please enter a valid link.",
        "downloading": "Downloading...",
        "done": "Download finished!",
        "open_folder": "Download in Browser",
        "no_history": "No history available.",
        "delete": "Delete",
        "format": "Format",
        "quality": "Quality",
        "shortcuts": "Shortcuts",
        "all_services_title": "All Supported Services",
        "clear_all": "Clear All",
        "saved_success": "Settings saved successfully!"
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
        "others": "Otros Servicios",
        "settings": "Ajustes",
        "history": "Historial",
        "btn_download": "Descargar",
        "video_audio": "Video + Audio",
        "audio_only": "Solo Audio",
        "video_only": "Solo Video",
        "best_quality": "Mejor Calidad",
        "select_folder": "Carpeta de Descarga en Servidor",
        "language_lbl": "Idioma de la Interfaz",
        "save_settings": "Guardar Ajustes",
        "empty_url": "Por favor, ingresa un enlace válido.",
        "downloading": "Descargando...",
        "done": "¡Descarga completada!",
        "open_folder": "Descargar en Navegador",
        "no_history": "No hay historial disponible.",
        "delete": "Eliminar",
        "format": "Formato",
        "quality": "Calidad",
        "shortcuts": "Atajos",
        "all_services_title": "Todos los Servicios Soportados",
        "clear_all": "Limpiar Todo",
        "saved_success": "¡Ajustes guardados correctamente!"
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
        "others": "Все сервисы",
        "settings": "Настройки",
        "history": "История",
        "btn_download": "Скачать",
        "video_audio": "Видео + Аудио",
        "audio_only": "Только Аудио",
        "video_only": "Только Видео",
        "best_quality": "Лучшее Качество",
        "select_folder": "Папка загрузки на сервере",
        "language_lbl": "Язык интерфейса",
        "save_settings": "Сохранить настройки",
        "empty_url": "Пожалуйста, введите правильную ссылку.",
        "downloading": "Скачивание...",
        "done": "Готово!",
        "open_folder": "Скачать в браузере",
        "no_history": "История недоступна.",
        "delete": "Удалить",
        "format": "Формат",
        "quality": "Качество",
        "shortcuts": "Ярлыки",
        "all_services_title": "Все поддерживаемые сервисы",
        "clear_all": "Очистить все",
        "saved_success": "Настройки успешно сохранены!"
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
        "others": "その他のサービス",
        "settings": "設定",
        "history": "履歴",
        "btn_download": "ダウンロード",
        "video_audio": "ビデオ + 音声",
        "audio_only": "音声のみ",
        "video_only": "ビデオのみ",
        "best_quality": "最高画質",
        "select_folder": "サーバーの保存先フォルダ",
        "language_lbl": "インターフェース言語",
        "save_settings": "設定を保存",
        "empty_url": "有効なリンクを入力してください。",
        "downloading": "ダウンロード中...",
        "done": "完了！",
        "open_folder": "ブラウザでダウンロード",
        "no_history": "履歴はありません。",
        "delete": "削除",
        "format": "フォーマット",
        "quality": "画質",
        "shortcuts": "ショートカット",
        "all_services_title": "サポートされているすべてのサービス",
        "clear_all": "すべて消去",
        "saved_success": "設定が正常に保存されました！"
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
        "others": "所有服务",
        "settings": "设置",
        "history": "历史记录",
        "btn_download": "下载",
        "video_audio": "视频 + 音频",
        "audio_only": "仅音频",
        "video_only": "仅视频",
        "best_quality": "最佳画质",
        "select_folder": "服务器下载文件夹",
        "language_lbl": "界面语言",
        "save_settings": "保存设置",
        "empty_url": "请输入有效的链接。",
        "downloading": "下载中...",
        "done": "下载完成！",
        "open_folder": "在浏览器中下载",
        "no_history": "暂无历史记录。",
        "delete": "删除",
        "format": "格式",
        "quality": "画质",
        "shortcuts": "快捷方式",
        "all_services_title": "所有支持的服务",
        "clear_all": "清空全部",
        "saved_success": "设置保存成功！"
    }
};

const SERVICE_EMOJIS = {
    "youtube": "▷", "spotify": "🎵", "tiktok": "📱", "instagram": "📸",
    "twitter": "🐦", "reddit": "👽", "pinterest": "📌", "facebook": "📘",
    "kwai": "🔥", "vimeo": "🎬", "twitch": "🟪", "soundcloud": "☁️",
    "bandcamp": "🎸", "bilibili": "📺"
};

// Initialize Application
document.addEventListener("DOMContentLoaded", async () => {
    await loadInitialData();
    setupEventListeners();
});

function getClientConfig(serverConfig = {}) {
    try {
        const localRaw = localStorage.getItem("paroni_client_config");
        if (localRaw) {
            return { ...serverConfig, ...JSON.parse(localRaw) };
        }
    } catch (e) {
        console.error("Local config parse error:", e);
    }
    return {
        download_folder: "temp",
        language: serverConfig.language || "Português",
        theme: serverConfig.theme || "system",
        shortcuts: serverConfig.shortcuts || ["youtube", "spotify", "tiktok", "instagram"]
    };
}

function saveClientConfig(configData) {
    currentConfig = { ...currentConfig, ...configData };
    try {
        localStorage.setItem("paroni_client_config", JSON.stringify(currentConfig));
    } catch (e) {
        console.error("Save client config error:", e);
    }
}

async function loadInitialData() {
    try {
        const [configRes, servicesRes] = await Promise.all([
            fetch("/api/config"),
            fetch("/api/services")
        ]);
        
        const serverConfig = await configRes.json();
        availableServices = await servicesRes.json();

        currentConfig = getClientConfig(serverConfig);

        renderSidebarShortcuts();
        renderServicesGrid();
        populateSettingsForm();
        applyTranslations(currentConfig.language || "Português");
        selectService(currentConfig.shortcuts?.[0] || "youtube");

        checkMasterStatus();

    } catch (e) {
        console.error("Failed to connect to backend server:", e);
    }
}

function setupEventListeners() {
    // Navigation Panel Buttons (Desktop & Mobile)
    document.querySelectorAll(".nav-btn, .mobile-nav-btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
            const viewTarget = btn.dataset.view;
            if (viewTarget) {
                switchView(viewTarget);
            }
        });
    });

    // Paste button
    document.getElementById("paste-btn").addEventListener("click", async () => {
        try {
            const text = await navigator.clipboard.readText();
            document.getElementById("url-input").value = text;
        } catch (err) {
            console.error("Clipboard paste error:", err);
        }
    });

    // Download Button
    document.getElementById("download-btn").addEventListener("click", startDownload);

    // Clear All History Button
    document.getElementById("clear-all-history-btn").addEventListener("click", clearAllHistory);

    // Save Settings Button
    document.getElementById("save-settings-btn").addEventListener("click", saveSettings);
    
    // Language Change trigger live translation
    document.getElementById("language-select").addEventListener("change", (e) => {
        applyTranslations(e.target.value);
    });

    // Format selection lock for audio-only services
    document.getElementById("format-select").addEventListener("change", updateFormatOptionLock);

    // Master Settings Listeners
    const unlockBtn = document.getElementById("unlock-master-btn");
    if (unlockBtn) unlockBtn.addEventListener("click", unlockMasterSection);

    const saveMasterBtn = document.getElementById("save-master-config-btn");
    if (saveMasterBtn) saveMasterBtn.addEventListener("click", saveMasterConfig);

    const restartBtn = document.getElementById("restart-server-btn");
    if (restartBtn) restartBtn.addEventListener("click", () => executeServerControl("restart"));

    const stopBtn = document.getElementById("stop-server-btn");
    if (stopBtn) stopBtn.addEventListener("click", () => executeServerControl("stop"));

    const changePinBtn = document.getElementById("change-pin-btn");
    if (changePinBtn) changePinBtn.addEventListener("click", changeMasterPinPrompt);
}

function switchView(viewId) {
    document.querySelectorAll(".view-panel").forEach(panel => {
        panel.classList.remove("active");
    });
    
    const targetPanel = document.getElementById(`view-${viewId}`);
    if (targetPanel) {
        targetPanel.classList.add("active");
    }

    // Sync active state on navigation buttons (Desktop & Mobile)
    document.querySelectorAll(".nav-btn, .mobile-nav-btn").forEach(btn => {
        if (btn.dataset.view === viewId) {
            btn.classList.add("active");
        } else {
            btn.classList.remove("active");
        }
    });

    if (viewId === "history") {
        fetchHistory();
    }
}

function renderSidebarShortcuts() {
    const container = document.getElementById("sidebar-shortcuts");
    container.innerHTML = "";
    
    const shortcuts = currentConfig.shortcuts || ["youtube", "spotify", "tiktok", "instagram"];
    
    shortcuts.forEach(serviceId => {
        const srv = availableServices.find(s => s.id === serviceId) || { id: serviceId, name: serviceId };
        const emoji = SERVICE_EMOJIS[srv.id] || "🔌";
        
        const btn = document.createElement("button");
        btn.className = "nav-btn";
        btn.dataset.service = srv.id;
        btn.innerHTML = `
            <span class="nav-icon">${emoji}</span>
            <span class="nav-text">${srv.name}</span>
        `;
        btn.addEventListener("click", () => {
            selectService(srv.id);
            document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
        });
        container.appendChild(btn);
    });

    // Highlight first shortcut
    const firstBtn = container.querySelector(".nav-btn");
    if (firstBtn) firstBtn.classList.add("active");
}

function selectService(serviceId) {
    activeService = serviceId;
    const srv = availableServices.find(s => s.id === serviceId) || { id: serviceId, name: serviceId };
    const emoji = SERVICE_EMOJIS[srv.id] || "🔌";
    
    document.getElementById("current-service-icon").textContent = emoji;
    
    const langDict = LANGUAGES[currentConfig.language || "Português"] || LANGUAGES["Português"];
    const titleKey = srv.id;
    document.getElementById("downloader-title").textContent = langDict[titleKey] || `${srv.name} Downloader`;
    
    const placeholderKey = srv.placeholder;
    document.getElementById("url-input").placeholder = langDict[placeholderKey] || `Cole o link do ${srv.name} aqui...`;
    
    // Auto adjust format for audio only services
    const formatSelect = document.getElementById("format-select");
    if (srv.video === false) {
        formatSelect.value = "audio_only";
        formatSelect.disabled = true;
    } else {
        formatSelect.disabled = false;
        formatSelect.value = "video_audio";
    }

    switchView("downloader");
}

function updateFormatOptionLock() {
    const srv = availableServices.find(s => s.id === activeService);
    if (srv && srv.video === false) {
        document.getElementById("format-select").value = "audio_only";
    }
}

function renderServicesGrid() {
    const grid = document.getElementById("services-grid");
    grid.innerHTML = "";

    availableServices.forEach(srv => {
        const emoji = SERVICE_EMOJIS[srv.id] || "🔌";
        const tag = (srv.video && srv.audio) ? "Vídeo e Áudio" : (srv.audio ? "Apenas Áudio" : "Vídeo");

        const card = document.createElement("div");
        card.className = "service-card";
        card.innerHTML = `
            <div class="service-card-icon">${emoji}</div>
            <div class="service-card-title">${srv.name}</div>
            <div class="service-card-tag">${tag}</div>
        `;
        card.addEventListener("click", () => {
            selectService(srv.id);
        });
        grid.appendChild(card);
    });
}

async function startDownload() {
    const url = document.getElementById("url-input").value.trim();
    const format = document.getElementById("format-select").value;
    const quality = document.getElementById("quality-select").value;

    const langDict = LANGUAGES[currentConfig.language || "Português"] || LANGUAGES["Português"];

    if (!url) {
        alert(langDict.empty_url || "Por favor, insira um link válido.");
        return;
    }

    const downloadBtn = document.getElementById("download-btn");
    const progressBox = document.getElementById("progress-container");
    const resultBox = document.getElementById("result-box");

    downloadBtn.disabled = true;
    progressBox.classList.remove("hidden");
    resultBox.classList.add("hidden");

    document.getElementById("progress-fill").style.width = "0%";
    document.getElementById("progress-percent").textContent = "0%";
    document.getElementById("status-text").textContent = langDict.downloading || "Iniciando download...";

    try {
        const res = await fetch("/api/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url, format, quality })
        });

        const data = await res.json();
        if (data.job_id) {
            activeJobId = data.job_id;
            pollJobProgress(activeJobId);
        } else {
            throw new Error(data.error || "Falha ao iniciar o download.");
        }
    } catch (err) {
        console.error("Download trigger error:", err);
        downloadBtn.disabled = false;
        document.getElementById("status-text").textContent = "Erro: " + err.message;
    }
}

function pollJobProgress(jobId) {
    if (pollTimer) clearInterval(pollTimer);

    pollTimer = setInterval(async () => {
        try {
            const res = await fetch(`/api/progress/${jobId}`);
            const job = await res.json();

            const percentInt = Math.round(job.progress * 100);
            document.getElementById("progress-fill").style.width = `${percentInt}%`;
            document.getElementById("progress-percent").textContent = `${percentInt}%`;
            document.getElementById("status-text").textContent = job.status_message || job.status;

            if (job.status === "finished") {
                clearInterval(pollTimer);
                document.getElementById("download-btn").disabled = false;
                document.getElementById("progress-container").classList.add("hidden");
                
                showDownloadResult(job);
                document.getElementById("url-input").value = "";
                fetchHistory(); // Refresh history
            } else if (job.status === "error") {
                clearInterval(pollTimer);
                document.getElementById("download-btn").disabled = false;
                document.getElementById("status-text").textContent = `Erro: ${job.error_message}`;
            }
        } catch (e) {
            console.error("Polling error:", e);
        }
    }, 800);
}

function showDownloadResult(job) {
    const resultBox = document.getElementById("result-box");
    const filenameOnly = job.final_path ? job.final_path.split(/[\\/]/).pop() : "media.mp4";
    const downloadUrl = `/api/files/${encodeURIComponent(filenameOnly)}`;

    document.getElementById("result-title").textContent = job.filename || "Arquivo Baixado";
    document.getElementById("result-path").textContent = "Enviado para o seu navegador! (O servidor apagará este arquivo temporário em 5 minutos)";
    
    const browserDownloadBtn = document.getElementById("browser-download-btn");
    browserDownloadBtn.href = downloadUrl;
    browserDownloadBtn.setAttribute("download", filenameOnly);
    browserDownloadBtn.innerHTML = "📥 Baixar Novamente";

    resultBox.classList.remove("hidden");

    // Add to local browser history
    addClientHistoryEntry(job);

    // Automatically trigger file download in browser
    try {
        const tempLink = document.createElement("a");
        tempLink.href = downloadUrl;
        tempLink.download = filenameOnly;
        document.body.appendChild(tempLink);
        tempLink.click();
        document.body.removeChild(tempLink);
    } catch (e) {
        console.error("Auto download trigger error:", e);
    }
}

// --- Per-Client Browser History (localStorage) ---
function getClientHistory() {
    try {
        const raw = localStorage.getItem("paroni_client_history");
        return raw ? JSON.parse(raw) : [];
    } catch (e) {
        return [];
    }
}

function saveClientHistory(historyArray) {
    try {
        localStorage.setItem("paroni_client_history", JSON.stringify(historyArray));
    } catch (e) {
        console.error("Save client history error:", e);
    }
}

function addClientHistoryEntry(job) {
    const history = getClientHistory();
    const filenameOnly = job.final_path ? job.final_path.split(/[\\/]/).pop() : job.filename;
    const entry = {
        name: job.filename || "Arquivo Baixado",
        service: job.service || "MÍDIA",
        duration: job.duration || "",
        link: job.url || "",
        path: filenameOnly,
        timestamp: Date.now()
    };
    const filtered = history.filter(h => h.link !== entry.link || h.name !== entry.name);
    filtered.unshift(entry);
    saveClientHistory(filtered.slice(0, 50));
}

function fetchHistory() {
    const historyData = getClientHistory();
    renderHistoryList(historyData);
}

function renderHistoryList(historyItems) {
    const container = document.getElementById("history-list");
    const emptyState = document.getElementById("empty-history");
    container.innerHTML = "";

    if (!historyItems || historyItems.length === 0) {
        emptyState.classList.remove("hidden");
        return;
    }

    emptyState.classList.add("hidden");

    historyItems.forEach(item => {
        const filenameOnly = item.path ? item.path.split(/[\\/]/).pop() : item.name;
        
        const el = document.createElement("div");
        el.className = "history-item";
        el.innerHTML = `
            <div class="history-item-info">
                <div class="history-item-header">
                    <span class="history-item-badge">${item.service || "MÍDIA"}</span>
                    <div class="history-item-name">${item.name}</div>
                </div>
                <div class="history-item-meta">
                    ${item.duration ? item.duration + " | " : ""} ${item.link || item.path}
                </div>
            </div>
            <div class="history-item-actions">
                <a href="/api/files/${encodeURIComponent(filenameOnly)}" download="${filenameOnly}" class="secondary-btn" title="Baixar Arquivo">📥</a>
                <button class="danger-btn" onclick="deleteHistoryEntry('${encodeURIComponent(item.link || item.path || item.name)}')">🗑️</button>
            </div>
        `;
        container.appendChild(el);
    });
}

function deleteHistoryEntry(linkOrPath) {
    const decoded = decodeURIComponent(linkOrPath);
    const history = getClientHistory();
    const updated = history.filter(item => item.link !== decoded && item.path !== decoded && item.name !== decoded);
    saveClientHistory(updated);
    renderHistoryList(updated);
}

function clearAllHistory() {
    if (!confirm("Deseja realmente limpar o histórico deste navegador?")) return;
    saveClientHistory([]);
    renderHistoryList([]);
}

function populateSettingsForm() {
    const folderInput = document.getElementById("download-folder-input");
    if (folderInput) folderInput.value = currentConfig.download_folder || "";
    document.getElementById("language-select").value = currentConfig.language || "Português";

    const shortcuts = currentConfig.shortcuts || ["youtube", "spotify", "tiktok", "instagram"];
    for (let i = 0; i < 4; i++) {
        const picker = document.getElementById(`shortcut-${i}`);
        if (!picker) continue;
        picker.innerHTML = "";
        availableServices.forEach(srv => {
            const opt = document.createElement("option");
            opt.value = srv.id;
            opt.textContent = srv.name;
            if (shortcuts[i] === srv.id) opt.selected = true;
            picker.appendChild(opt);
        });
    }
}

async function saveSettings() {
    const language = document.getElementById("language-select").value;
    
    const newShortcuts = [];
    for (let i = 0; i < 4; i++) {
        const picker = document.getElementById(`shortcut-${i}`);
        if (picker) newShortcuts.push(picker.value);
    }

    saveClientConfig({
        language: language,
        shortcuts: newShortcuts
    });

    renderSidebarShortcuts();
    applyTranslations(currentConfig.language);

    const statusEl = document.getElementById("settings-status");
    const langDict = LANGUAGES[currentConfig.language] || LANGUAGES["Português"];
    statusEl.textContent = langDict.saved_success || "Configurações salvas neste dispositivo!";
    setTimeout(() => { statusEl.textContent = ""; }, 3000);
}

function applyTranslations(lang) {
    const t = LANGUAGES[lang] || LANGUAGES["Português"];
    currentConfig.language = lang;

    // Static text mappings
    const mappings = {
        "lbl-shortcuts": t.shortcuts,
        "txt-others": t.others,
        "txt-history": t.history,
        "txt-settings": t.settings,
        "lbl-format-type": t.format,
        "lbl-quality-type": t.quality,
        "txt-btn-download": t.btn_download,
        "txt-title-others": t.all_services_title,
        "txt-title-history": t.history,
        "clear-all-history-btn": t.clear_all,
        "txt-empty-history": t.no_history,
        "txt-title-settings": t.settings,
        "txt-lbl-download-folder": t.select_folder,
        "txt-lbl-app-lang": t.language_lbl,
        "txt-lbl-shortcuts-config": t.shortcuts,
        "txt-btn-save-settings": t.save_settings,
        "opt-video-audio": t.video_audio,
        "opt-audio-only": t.audio_only,
        "opt-video-only": t.video_only,
        "opt-best-quality": t.best_quality
    };

    Object.keys(mappings).forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            if (el.tagName === "OPTION") el.text = mappings[id];
            else el.textContent = mappings[id];
        }
    });

    // Update active service title and placeholder
    const srv = availableServices.find(s => s.id === activeService);
    if (srv) {
        document.getElementById("downloader-title").textContent = t[srv.id] || `${srv.name} Downloader`;
        document.getElementById("url-input").placeholder = t[srv.placeholder] || `Cole o link do ${srv.name} aqui...`;
    }
}

// --- Master Settings & Server Control ---
let unlockedMasterPin = null;

async function checkMasterStatus() {
    try {
        const res = await fetch("/api/master/status");
        const status = await res.json();
        
        const pinHint = document.getElementById("master-pin-hint");
        const unlockBtn = document.getElementById("unlock-master-btn");
        const pinInput = document.getElementById("master-pin-input");

        if (!status.has_pin) {
            if (pinHint) pinHint.textContent = "Nenhum PIN Mestre configurado ainda. Digite um PIN de no mínimo 4 dígitos abaixo para criar e proteger este servidor.";
            if (pinInput) pinInput.placeholder = "Crie o PIN Mestre...";
            if (unlockBtn) unlockBtn.textContent = "Criar PIN";
        } else {
            if (pinHint) pinHint.textContent = "Insira o PIN Mestre para desbloquear os controles avançados do servidor (Porta, Modo IP e Servidor).";
            if (pinInput) pinInput.placeholder = "Digite o PIN Mestre...";
            if (unlockBtn) unlockBtn.textContent = "Desbloquear";
        }

        const currentPort = status.port || 3000;
        const portInput = document.getElementById("master-port-input");
        if (portInput) portInput.value = currentPort;
        
        const bindSelect = document.getElementById("master-bind-select");
        if (bindSelect) bindSelect.value = status.bind_address || "0.0.0.0";

        const badge = document.getElementById("server-status-badge");
        if (badge) {
            badge.textContent = `Online :${currentPort}`;
            badge.title = `Servidor rodando em ${status.bind_address || "0.0.0.0"}:${currentPort}`;
        }

    } catch (e) {
        console.error("Failed to fetch master status:", e);
    }
}

async function unlockMasterSection() {
    const pinInput = document.getElementById("master-pin-input");
    const errorEl = document.getElementById("master-login-error");
    const pin = pinInput ? pinInput.value.trim() : "";

    if (errorEl) errorEl.textContent = "";

    if (!pin || pin.length < 4) {
        if (errorEl) errorEl.textContent = "O PIN deve ter no mínimo 4 dígitos.";
        return;
    }

    try {
        const statusRes = await fetch("/api/master/status");
        const status = await statusRes.json();

        if (!status.has_pin) {
            // First time PIN setup
            const saveRes = await fetch("/api/master/save_pin", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ current_pin: "", new_pin: pin })
            });
            const saveData = await saveRes.json();

            if (saveData.success) {
                unlockedMasterPin = pin;
                showMasterUnlockedState();
            } else {
                if (errorEl) errorEl.textContent = saveData.error || "Falha ao salvar PIN.";
            }
        } else {
            // Verify existing PIN
            const verifyRes = await fetch("/api/master/verify_pin", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ pin: pin })
            });
            const verifyData = await verifyRes.json();

            if (verifyData.success) {
                unlockedMasterPin = pin;
                showMasterUnlockedState();
            } else {
                if (errorEl) errorEl.textContent = verifyData.error || "PIN incorreto.";
            }
        }
    } catch (e) {
        if (errorEl) errorEl.textContent = "Erro ao se comunicar com o servidor.";
    }
}

function showMasterUnlockedState() {
    const loginBox = document.getElementById("master-login-box");
    if (loginBox) loginBox.classList.add("hidden");
    
    const controlsBox = document.getElementById("master-controls-box");
    if (controlsBox) controlsBox.classList.remove("hidden");
    
    const lockBadge = document.getElementById("master-lock-status");
    if (lockBadge) {
        lockBadge.textContent = "🔓 Desbloqueado";
        lockBadge.className = "lock-badge unlocked";
    }
}

async function saveMasterConfig() {
    if (!unlockedMasterPin) return;

    const port = document.getElementById("master-port-input").value;
    const bind_address = document.getElementById("master-bind-select").value;
    const statusMsg = document.getElementById("master-status-msg");

    if (statusMsg) {
        statusMsg.style.color = "#34d399";
        statusMsg.textContent = "Salvando...";
    }

    try {
        const res = await fetch("/api/master/config", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                pin: unlockedMasterPin,
                port: parseInt(port, 10),
                bind_address: bind_address
            })
        });

        const data = await res.json();
        if (data.success) {
            if (statusMsg) statusMsg.textContent = data.message || "Configuração Mestre salva! Reinicie o servidor para aplicar a nova porta/host.";
        } else {
            if (statusMsg) {
                statusMsg.style.color = "#f87171";
                statusMsg.textContent = data.error || "Falha ao salvar.";
            }
        }
    } catch (e) {
        if (statusMsg) {
            statusMsg.style.color = "#f87171";
            statusMsg.textContent = "Erro ao salvar configuração mestre.";
        }
    }
}

async function executeServerControl(action) {
    if (!unlockedMasterPin) return;

    const actionText = action === "stop" ? "desligar" : "reiniciar";
    if (!confirm(`Deseja realmente ${actionText} o servidor?`)) return;

    const statusMsg = document.getElementById("master-status-msg");
    if (statusMsg) {
        statusMsg.style.color = "#fbbf24";
        statusMsg.textContent = `Enviando comando para ${actionText} o servidor...`;
    }

    try {
        const res = await fetch("/api/master/server_control", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                pin: unlockedMasterPin,
                action: action
            })
        });

        const data = await res.json();
        if (data.success) {
            if (statusMsg) {
                statusMsg.style.color = "#34d399";
                statusMsg.textContent = data.message || `Servidor ${actionText}ado com sucesso.`;
            }
        } else {
            if (statusMsg) {
                statusMsg.style.color = "#f87171";
                statusMsg.textContent = data.error || "Falha na ação.";
            }
        }
    } catch (e) {
        if (statusMsg) {
            statusMsg.style.color = "#34d399";
            statusMsg.textContent = `Comando enviado! Servidor ${actionText}ado.`;
        }
    }
}

async function changeMasterPinPrompt() {
    if (!unlockedMasterPin) return;
    const newPin = prompt("Digite o novo PIN Mestre (mínimo 4 dígitos):");
    if (!newPin || newPin.length < 4) {
        alert("O PIN deve ter no mínimo 4 dígitos.");
        return;
    }

    try {
        const res = await fetch("/api/master/save_pin", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ current_pin: unlockedMasterPin, new_pin: newPin })
        });
        const data = await res.json();
        if (data.success) {
            unlockedMasterPin = newPin;
            alert("PIN Mestre alterado com sucesso!");
        } else {
            alert(data.error || "Falha ao alterar o PIN.");
        }
    } catch (e) {
        alert("Erro de comunicação ao alterar PIN.");
    }
}
