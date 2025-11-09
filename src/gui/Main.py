import os
import threading
import webview
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from Api import API

# ----------------------------------------------------
# 1️⃣ Choix de la racine pour le mini serveur HTTP
# ----------------------------------------------------
WEB_ROOT = os.path.abspath("html")
PORT = 8000

os.chdir(WEB_ROOT)

# ----------------------------------------------------
# 2️⃣ Serveur HTTP dans un thread séparé
# ----------------------------------------------------
class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

httpd = TCPServer(("", PORT), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()

# ----------------------------------------------------
# Crée la fenêtre WebView
# ----------------------------------------------------
api_instance = API()

window = webview.create_window(
    "AbsolutWarehouse",
    f"http://127.0.0.1:{PORT}/pages/index.html",
    width=1000,
    height=600,
    resizable=True,
    js_api=api_instance  # ← expose l'API à JS
)

webview.start(gui='gtk', debug=False)
