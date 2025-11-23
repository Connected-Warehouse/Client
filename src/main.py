import threading
import time
from datetime import date, datetime

from client.SocketClient import SocketClient
from client.listener.MyListener import MyListener

# ======================
# LISTENER
# ======================
class ScenarioListener(MyListener):
    def on_connected(self):
        print("[INFO] Connected to server.")

    def on_disconnected(self):
        print("[INFO] Disconnected from server.")

    def on_received(self, message: str):
        # Affiche chaque message reçu directement
        print("[RECEIVED]", message.strip())

    def on_error(self, error: Exception):
        print(f"[ERROR] {error}")


def send_and_wait(client: SocketClient, listener: ScenarioListener, message: str, timeout=1.0):
    """
    Envoie un message au serveur.
    Comme le listener affiche les messages directement,
    on ne retourne plus de bloc complet.
    """
    print(f"[SENDING] {message}")
    client.send_message(message)
    time.sleep(timeout)  # Petit délai pour laisser le serveur répondre


# ======================
# TESTS SCÉNARIOS
# ======================

TERMINAL_NAME = "A001"

def scenario_command(host, port, command_type, **kwargs):
    """
    Envoie une commande au serveur pour un package donné avec des arguments optionnels.

    :param host: serveur
    :param port: port serveur
    :param command_type: "ADD", "READ", "DELETE", "MODIFY"
    :param package_code: code du package
    :param kwargs: dictionnaire des champs optionnels, ex: fragile=True, weight=10
    """
    listener = ScenarioListener()
    client = SocketClient(host, port, listener)
    client.connect()

    if not client.connected:
        print("[ERROR] Server rejected us.")
        return

    # Envoyer la commande principale avec le package_code
    send_and_wait(client, listener, f"{command_type} {TERMINAL_NAME}")

    # Construire la ligne d'arguments optionnels
    args_list = []
    for key, value in kwargs.items():
        if value is None:
            continue
        if isinstance(value, bool):
            value = str(value).lower()
        args_list.append(f"-{key} {value}")

    # Envoyer les arguments si présents
    if args_list:
        send_and_wait(client, listener, " ".join(args_list))

    client.disconnect()








# ======================
# MAIN
# ======================
def main():
    host = "127.0.0.1"
    port = 8888

    print("Premier scénario : Ajout d'une commande")
    scenario_command(host,port,"ADD",code="PKG111",
                     fragile=False,
                     refrigerated=False,
                     spacecode="E403",
                     destination=156,
                     source=43,
                     weight=10,
                     estimated_delivery=f"{date(2025, 10, 23)}",
                     )

    print("Deuxième scénario : Lecture d'une commande")
    scenario_command(host, port, "READ", code="PKG111")

    print("Troisième scénario : Modification d'une commande")
    scenario_command(host, port, "MODIFY", code="PKG111",
                     fragile=True,
                     refrigerated=True,
                     spacecode="B102",
                     destination=11,
                     source=40,
                     weight=235,
                     status="delivered",
                     estimated_delivery=f"{date(2025, 12, 5)}",
                     exit_time="now"
                     )

    print("Quatrième scénario : Relecture d'une commande modifié")
    scenario_command(host, port, "READ", code="PKG111")

    print("Cinquième scénario : Suppression d'une commande")
    scenario_command(host, port, "DELETE", code="PKG111")

if __name__ == "__main__":
    main()
