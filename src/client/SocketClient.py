import socket
import threading
from typing import Optional
from client.listener import MyListener

class SocketClient:
    def __init__(self, host: str, port: int, listener: MyListener):
        self.host = host
        self.port = port
        self.listener = listener
        self.sock: Optional[socket.socket] = None

        self.running = False
        self.recv_thread: Optional[threading.Thread] = None
        self.connected = False
        self.lock = threading.Lock()

    # =======================================================
    # CONNEXION
    # =======================================================
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))

            with self.lock:
                self.connected = True
                self.running = True

            if self.listener:
                self.listener.on_connected()

            self.recv_thread = threading.Thread(
                target=self._recv_loop, daemon=True
            )
            self.recv_thread.start()
        except socket.gaierror as e:
            print("[DNS ERROR] Failed to resolve host:", self.host)

        except Exception as e:
            if self.listener:
                self.listener.on_error(e)

    # =======================================================
    # ENVOI DE MESSAGE
    # =======================================================
    def send_message(self, message: str):
        if not self.connected or not self.sock:
            raise RuntimeError("Pas connecté au serveur")

        try:
            self.sock.sendall((message + "\n").encode("utf-8"))
        except Exception as e:
            if self.listener:
                self.listener.on_error(e)

    # =======================================================
    # BOUCLE DE RECEPTION
    # =======================================================
    def _recv_loop(self):
        try:
            if not self.sock:
                return

            # Utilisation de makefile pour lecture ligne par ligne
            with self.sock.makefile('r', encoding='latin-1') as f:
                while True:
                    with self.lock:
                        if not self.running or not self.connected:
                            break

                    line = f.readline()
                    if not line:
                        break  # serveur fermé

                    msg = line.strip()
                    if self.listener:
                        self.listener.on_received(msg)

        except Exception as e:
            if self.listener:
                self.listener.on_error(e)

        finally:
            # déconnexion propre
            self._internal_disconnect()

    # =======================================================
    # DECONNEXION INTERNE (appelée une seule fois)
    # =======================================================
    def _internal_disconnect(self):
        """ Assure une déconnexion unique et sûre. """
        with self.lock:
            if not self.connected:
                return  # déjà déconnecté

            self.connected = False
            self.running = False

        # fermer le socket
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                self.sock.close()
            except:
                pass
            self.sock = None

        if self.listener:
            self.listener.on_disconnected()

    # =======================================================
    # DECONNEXION DEMANDÉE PAR L'UTILISATEUR
    # =======================================================
    def disconnect(self):
        """Appelé par le code utilisateur."""
        self._internal_disconnect()
