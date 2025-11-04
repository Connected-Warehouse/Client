import socket
import threading
from typing import Optional
from client.listener import MyListener

class SocketClient:
    def __init__(self, host: str, port: int, listener : MyListener):
        self.host = host
        self.port = port
        self.listener = listener
        self.sock: Optional[socket.socket] = None
        self._running = False
        self._recv_thread: Optional[threading.Thread] = None

    def connect(self):
        """Se connecter au serveur et démarrer le thread de réception"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self._running = True
            if self.listener:
                self.listener.on_connected()

            # démarrer le thread d'écoute des messages
            self._recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
            self._recv_thread.start()
        except Exception as e:
            if self.listener:
                self.listener.on_error(e)

    def send_message(self, message: str):
        """Envoyer un message au serveur"""
        if not self.sock:
            raise RuntimeError("Pas connecté au serveur")
        try:
            self.sock.sendall((message + "\n").encode('utf-8'))
        except Exception as e:
            if self.listener:
                self.listener.on_error(e)

    def _recv_loop(self):
        """Boucle de réception des messages du serveur"""
        try:
            while self._running and self.sock:
                data = self.sock.recv(1024)
                if not data:
                    break  # serveur a fermé la connexion
                message = data.decode('utf-8').strip()
                if self.listener:
                    self.listener.on_received(message)
        except Exception as e:
            if self.listener:
                self.listener.on_error(e)
        finally:
            self._running = False
            if self.listener:
                self.listener.on_disconnected()
            self.disconnect()  # fermeture propre

    def disconnect(self):
        """Déconnecter proprement"""
        self._running = False
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
            if self.listener:
                self.listener.on_disconnected()
