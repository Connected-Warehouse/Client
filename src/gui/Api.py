import threading
import time

from client.SocketClient import SocketClient
from client.listener.MyListener import MyListener
from gui.config import load_config


class API:
    RESPONSE_TIMEOUT = 2  # secondes à attendre pour la réponse du serveur

    def __init__(self, host="127.0.0.1", port=8888):
        self.host = host
        self.port = port
        self.listener = None
        self.client = None
        self.connected = False
        self.lock = threading.Lock()  # sécuriser l'accès aux messages

    def connect(self):
        """Connexion TCP au serveur, appelée manuellement."""
        if self.connected:
            return True
        try:
            self.listener = MyListener()
            self.client = SocketClient(self.host, self.port, self.listener)
            self.client.connect()
            self.connected = True
            print("[API] Connecté au serveur TCP", flush=True)
            return True
        except Exception as e:
            print("[API] Erreur de connexion :", e, flush=True)
            self.connected = False
            return False

    def disconnect(self):
        if self.client:
            self.client.disconnect()
        self.connected = False
        print("[API] Déconnecté du serveur TCP", flush=True)

    def safeDisconnect(self):
        if self.connected and self.client:
            try:
                # Envoyer la commande de déconnexion
                self.client.send_message("DISCONNECT")
                print("[API] Message DISCONNECT envoyé")
            except Exception as e:
                print("[API] Erreur en envoyant DISCONNECT :", e)
            try:
                self.client.disconnect()
                print("[API] Client déconnecté proprement")
            except Exception as e:
                print("[API] Erreur en déconnectant le client :", e)
            self.connected = False

    # -------------------------
    # Méthodes pour les menus
    # -------------------------
    def loadAddMenu(self):
        return self._send_menu_command("ADD")

    def loadDeleteMenu(self):
        return self._send_menu_command("DELETE")

    def loadModifyMenu(self):
        return self._send_menu_command("MODIFY")

    def loadSearchMenu(self):
        return self._send_menu_command("SEARCH")

    def modify_package(self, data):
        message = (
            f"{data.get('code', '')} "
            f"{data.get('zone', '')} "
            f"{data.get('provenance', '')} "
            f"{data.get('destination', '')} "
            f"{data.get('weigth', '')} "
            f"{'REFRIGERATED' if data.get('refrigerated') else ''} "
            f"{'FRAGILE' if data.get('fragile') else ''}"
        ).strip()
        print(message)
        return self._send_command(message)

    def add_package(self, data):
        message = (
            f"{data.get('code', '')} "
            f"{data.get('zone', '')} "
            f"{data.get('provenance', '')} "
            f"{data.get('destination', '')} "
            f"{data.get('weigth', '')} "
            f"{'REFRIGERATED' if data.get('refrigerated') else ''} "
            f"{'FRAGILE' if data.get('fragile') else ''}"
        ).strip()
        print(message)
        return self._send_command(message)

    def remove_package(self, data):
        message = f"{data.get('code', '')}"
        print(message)
        return self._send_command(message)

    def search_package(self, data):
        message = f"{data.get('code', '')}"
        print(message)
        return self._send_command(message)

    # -------------------------
    # Méthode générique
    # -------------------------

    def _send_command(self, text):
        print(f"[API] Command '{text}' called", flush=True)
        if not self.connected:
            if not self.connect():
                return None  # ou "DENIED" si tu veux un retour par défaut

        message = text
        with self.lock:
            try:
                self.listener.last_response = None  # réinitialiser
                self.client.send_message(message)
                print(f"[API] Message envoyé : {message}", flush=True)

                start_time = time.time()
                while time.time() - start_time < self.RESPONSE_TIMEOUT:
                    response = getattr(self.listener, "last_response", None)
                    if response is not None:
                        response = response.strip()
                        print(f"[API] Réponse reçue : {response}", flush=True)
                        return response  # <-- on retourne directement la réponse brute
                    time.sleep(0.05)

                print("[API] Timeout, pas de réponse du serveur", flush=True)
                return None
            except Exception as e:
                print("[API] Erreur en envoyant la commande :", e, flush=True)
                return None

    def _send_menu_command(self, command):
        print(f"[API] Command {command} called", flush=True)
        if not self.connected:
            if not self.connect():
                return "DENIED"

        message = f"{command} {self.getMachine()}"
        with self.lock:
            try:
                self.listener.last_response = None  # <-- réinitialiser
                self.client.send_message(message)
                print(f"[API] Message envoyé : {message}", flush=True)

                start_time = time.time()
                while time.time() - start_time < self.RESPONSE_TIMEOUT:
                    response = getattr(self.listener, "last_response", None)
                    if response is not None:
                        response = response.strip()
                        print(f"[API] Réponse reçue : {response}", flush=True)
                        return "AUTHORIZED" if response.upper() == "ALLOWED" else "DENIED"
                    time.sleep(0.05)

                print("[API] Timeout, pas de réponse du serveur", flush=True)
                return "DENIED"
            except Exception as e:
                print("[API] Erreur en envoyant la commande :", e, flush=True)
                return "DENIED"

    def getMachine(self):
        config = load_config()
        return config.get("machine", "UNKNOWN")
