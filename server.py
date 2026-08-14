import os
import sys
import json
import socket
import urllib.parse
import mimetypes
from http.server import HTTPServer, ThreadingHTTPServer, SimpleHTTPRequestHandler

# Import modular downloader core engine
from downloader_core import ConfigManager, engine_instance, SERVICES_METADATA

PORT = 3000
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")

def get_local_ip():
    """Retrieve the primary local LAN IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class ParoniDownloaderHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP Request Handler serving Web UI and REST API."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def _send_json_response(self, data, status_code=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, message, status_code=400):
        self._send_json_response({"error": message}, status_code=status_code)

    def _parse_json_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            raw_body = self.rfile.read(content_length).decode('utf-8')
            return json.loads(raw_body)
        return {}

    def do_OPTIONS(self):
        """CORS preflight request support."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        # REST API Routes
        if path == "/api/config":
            config = ConfigManager.load_config()
            self._send_json_response(config)
            return

        elif path == "/api/services":
            self._send_json_response(SERVICES_METADATA)
            return

        elif path == "/api/history":
            config = ConfigManager.load_config()
            self._send_json_response(config.get("history", []))
            return

        elif path.startswith("/api/progress/"):
            job_id = path.replace("/api/progress/", "").strip()
            job = engine_instance.get_job(job_id)
            if job:
                self._send_json_response(job.to_dict())
            else:
                self._send_error_json("Job not found", 404)
            return

        elif path == "/api/master/status":
            config = ConfigManager.load_config()
            master_pin = config.get("master_pin", "")
            self._send_json_response({
                "has_pin": bool(master_pin),
                "port": config.get("port", PORT),
                "bind_address": config.get("bind_address", "0.0.0.0")
            })
            return

        elif path.startswith("/api/files/"):
            filename = urllib.parse.unquote(path.replace("/api/files/", ""))
            temp_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
            file_path = os.path.join(temp_folder, filename)

            if not os.path.isfile(file_path):
                config = ConfigManager.load_config()
                download_folder = config.get("download_folder", ConfigManager.get_default_download_folder())
                file_path = os.path.join(download_folder, filename)

            if not os.path.isfile(file_path):
                self._send_error_json("Arquivo não encontrado ou já expirou do servidor (deletado após 5 min).", 404)
                return

            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type = mime_type or 'application/octet-stream'
            file_size = os.path.getsize(file_path)

            file_name = os.path.basename(file_path)
            encoded_filename = urllib.parse.quote(file_name)
            ext = os.path.splitext(file_name)[1] or ".mp4"

            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', str(file_size))
            self.send_header('Content-Disposition', f"attachment; filename=\"download{ext}\"; filename*=UTF-8''{encoded_filename}")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            with open(file_path, 'rb') as f:
                while chunk := f.read(65536):
                    self.wfile.write(chunk)
            return

        # Serve static web frontend files (index.html, styles.css, app.js)
        return super().do_GET()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == "/api/config":
            try:
                new_data = self._parse_json_body()
                config = ConfigManager.load_config()
                config.update(new_data)
                ConfigManager.save_config(config)
                self._send_json_response(config)
            except Exception as e:
                self._send_error_json(str(e))
            return

        elif path == "/api/download":
            try:
                payload = self._parse_json_body()
                url = payload.get("url", "")
                download_type = payload.get("format", "video_audio")
                quality = payload.get("quality", "best_quality")

                if not url:
                    self._send_error_json("URL parameter is required.")
                    return

                job_id = engine_instance.create_job(url, download_type, quality)
                self._send_json_response({"job_id": job_id})
            except Exception as e:
                self._send_error_json(str(e))
            return

        elif path == "/api/master/verify_pin":
            payload = self._parse_json_body()
            pin = payload.get("pin", "")
            config = ConfigManager.load_config()
            master_pin = config.get("master_pin", "")
            if not master_pin:
                self._send_json_response({"success": True, "no_pin_set": True})
            elif pin == master_pin:
                self._send_json_response({"success": True})
            else:
                self._send_error_json("PIN mestre incorreto.", 401)
            return

        elif path == "/api/master/save_pin":
            payload = self._parse_json_body()
            current_pin = payload.get("current_pin", "")
            new_pin = payload.get("new_pin", "")

            if not new_pin or len(new_pin) < 4:
                self._send_error_json("O PIN mestre deve ter no mínimo 4 dígitos.", 400)
                return

            config = ConfigManager.load_config()
            existing_pin = config.get("master_pin", "")

            if existing_pin and current_pin != existing_pin:
                self._send_error_json("PIN atual incorreto.", 401)
                return

            config["master_pin"] = new_pin
            ConfigManager.save_config(config)
            self._send_json_response({"success": True, "message": "PIN Mestre salvo com sucesso!"})
            return

        elif path == "/api/master/config":
            payload = self._parse_json_body()
            pin = payload.get("pin", "")
            config = ConfigManager.load_config()
            master_pin = config.get("master_pin", "")

            if master_pin and pin != master_pin:
                self._send_error_json("PIN mestre incorreto.", 401)
                return

            new_port = payload.get("port")
            new_bind = payload.get("bind_address")

            if new_port:
                try:
                    config["port"] = int(new_port)
                except ValueError:
                    self._send_error_json("Porta inválida.", 400)
                    return

            if new_bind in ["0.0.0.0", "127.0.0.1"]:
                config["bind_address"] = new_bind

            ConfigManager.save_config(config)
            self._send_json_response({"success": True, "message": "Configurações mestre salvas com sucesso!"})
            return

        elif path == "/api/master/server_control":
            payload = self._parse_json_body()
            pin = payload.get("pin", "")
            action = payload.get("action", "")
            config = ConfigManager.load_config()
            master_pin = config.get("master_pin", "")

            if master_pin and pin != master_pin:
                self._send_error_json("PIN mestre incorreto.", 401)
                return

            if action == "stop":
                self._send_json_response({"success": True, "message": "Desligando servidor..."})
                def _kill():
                    import time
                    time.sleep(0.5)
                    os._exit(0)
                import threading
                threading.Thread(target=_kill, daemon=True).start()
                return

            elif action == "restart":
                self._send_json_response({"success": True, "message": "Reiniciando servidor..."})
                def _restart():
                    import time, subprocess
                    time.sleep(0.5)
                    subprocess.Popen([sys.executable] + sys.argv)
                    os._exit(0)
                import threading
                threading.Thread(target=_restart, daemon=True).start()
                return

            self._send_error_json("Ação inválida.", 400)
            return

        self._send_error_json("Endpoint not found", 404)

    def do_DELETE(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == "/api/history":
            query_params = urllib.parse.parse_qs(parsed_path.query)
            if "all" in query_params:
                config = ConfigManager.load_config()
                config["history"] = []
                ConfigManager.save_config(config)
                self._send_json_response([])
            elif "item" in query_params:
                item_val = query_params["item"][0]
                updated_history = ConfigManager.delete_history_item(item_val)
                self._send_json_response(updated_history)
            else:
                self._send_error_json("Missing deletion query parameter")
            return

        self._send_error_json("Endpoint not found", 404)

    def log_message(self, format, *args):
        """Clean log output formatting."""
        sys.stderr.write(f"[Server] {self.address_string()} - {format % args}\n")

def run_server(port=None):
    config = ConfigManager.load_config()
    server_port = port if port is not None else config.get("port", PORT)
    host = config.get("bind_address", "0.0.0.0")

    server_address = (host, server_port)
    httpd = ThreadingHTTPServer(server_address, ParoniDownloaderHTTPRequestHandler)
    local_ip = get_local_ip()

    print("=" * 60)
    print("        PARONI DOWNLOADER - WEB SERVER (HEADLESS)")
    print("=" * 60)
    print(f"  [+] Headless server running on port {server_port}")
    print(f"  [+] Host bind:        {host}")
    print(f"  [+] Local access:     http://localhost:{server_port}")
    if host == "0.0.0.0":
        print(f"  [+] Network access:   http://{local_ip}:{server_port}")
    else:
        print("  [+] Mode:             Apenas Localhost (Acesso externo bloqueado)")
    print("=" * 60)
    print("  Press Ctrl+C to stop the server.\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] Stopping web server...")
        httpd.server_close()
        print("[+] Server stopped gracefully.")

if __name__ == "__main__":
    run_server()
