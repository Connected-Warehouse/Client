import time
from datetime import date

from client.SocketClient import SocketClient
from client.listener.MyListener import MyListener

# ======================
# LISTENER POUR LES SCÉNARIOS
# ======================
class ScenarioListener(MyListener):
    def on_connected(self):
        print("[INFO] Connected to server.")

    def on_disconnected(self):
        print("[INFO] Disconnected from server.")

    def on_received(self, message: str):
        print("[RECEIVED]", message.strip())

    def on_error(self, error: Exception):
        print(f"[ERROR] {error}")


# ======================
# FONCTION UTILE D'ENVOI DE MESSAGE
# ======================
def safe_send(client: SocketClient, listener: ScenarioListener, message: str, host="127.0.0.1", port=8888, timeout=1.0):
    """
    Envoie un message au serveur, reconnecte si nécessaire.
    """
    if client is None or not client.connected:
        print(f"[INFO] Client non connecté, tentative de reconnexion...")
        client = SocketClient(host, port, listener)
        client.connect()
        if not client.connected:
            print("[ERROR] Reconnexion échouée. On skip l'étape :", message)
            return client

    try:
        print(f"[SENDING] {message}")
        client.send_message(message)
        time.sleep(timeout)
    except Exception as e:
        print(f"[ERROR] Échec envoi message : {e}")
    return client


# ======================
# CONSTANTES
# ======================
TERMINAL_NAME = "A001"
PACKAGE_CODE = "PKG777"
HOST = "127.0.0.1"
PORT = 8888


# ======================
# SCÉNARIOS
# ======================

def scenario_1(host=HOST, port=PORT):
    """
    Scénario 1 : Ajout d'un package puis lecture puis suppression
    """
    listener = ScenarioListener()
    client = SocketClient(host, port, listener)
    client.connect()

    package_code = f"{PACKAGE_CODE}"
    total_steps = 3

    # --- Étape 1 : ADD ---
    step = 1
    print(f"[SCÉNARIO 1 - Étape {step}/{total_steps}] Ajout du colis...")
    client = safe_send(client, listener, f"ADD {TERMINAL_NAME}", host, port)
    args_add = f"-code {package_code} -fragile true -refrigerated false -spacecode E403 " \
               f"-source alex.durand@email.com -destination gogo@gmail.com " \
               f"-weight 10 -status in_storage -estimated_delivery {date(2025, 11, 30)}"
    client = safe_send(client, listener, args_add, host, port)
    input(f"[SCÉNARIO 1 - Étape {step}/{total_steps}] Terminé. Appuyez sur Entrée pour continuer...")

    # --- Étape 2 : READ ---
    step += 1
    print(f"[SCÉNARIO 1 - Étape {step}/{total_steps}] Lecture du colis ajouté...")
    client = safe_send(client, listener, f"READ {TERMINAL_NAME}", host, port)
    client = safe_send(client, listener, f"-code {package_code}", host, port)
    input(f"[SCÉNARIO 1 - Étape {step}/{total_steps}] Terminé. Appuyez sur Entrée pour continuer...")

    # --- Étape 3 : DELETE ---
    step += 1
    print(f"[SCÉNARIO 1 - Étape {step}/{total_steps}] Suppression du colis...")
    client = safe_send(client, listener, f"DELETE {TERMINAL_NAME}", host, port)
    client = safe_send(client, listener, f"-code {package_code}", host, port)
    input(f"[SCÉNARIO 1 - Étape {step}/{total_steps}] Terminé. Fin du scénario 1. Appuyez sur Entrée pour continuer...")

    client.disconnect()


def scenario_2(host=HOST, port=PORT):
    """
    Scénario 2 : Ajout, lecture, modification, lecture, suppression, lecture
    """
    listener = ScenarioListener()
    client = SocketClient(host, port, listener)
    client.connect()

    package_code = f"{PACKAGE_CODE}"
    total_steps = 6
    step = 1

    # --- Étape 1 : ADD ---
    print(f"[SCÉNARIO 2 - Étape {step}/{total_steps}] Ajout du colis...")
    client = safe_send(client, listener, f"ADD {TERMINAL_NAME}", host, port)
    args_add = f"-code {package_code} -fragile true -refrigerated false -spacecode E403 " \
               f"-source alex.durand@email.com -destination gogo@gmail.com " \
               f"-weight 10 -status in_storage -estimated_delivery {date(2025, 11, 30)}"
    client = safe_send(client, listener, args_add, host, port)
    input(f"[SCÉNARIO 2 - Étape {step}/{total_steps}] Terminé. Appuyez sur Entrée pour continuer...")

    # --- Étape 2 : READ après ADD ---
    step += 1
    print(f"[SCÉNARIO 2 - Étape {step}/{total_steps}] Lecture après ajout...")
    client = safe_send(client, listener, f"READ {TERMINAL_NAME}", host, port)
    client = safe_send(client, listener, f"-code {package_code}", host, port)
    input(f"[SCÉNARIO 2 - Étape {step}/{total_steps}] Terminé. Appuyez sur Entrée pour continuer...")

    # --- Étape 3 : MODIFY ---
    step += 1
    print(f"[SCÉNARIO 2 - Étape {step}/{total_steps}] Modification du colis...")
    client = safe_send(client, listener, f"MODIFY {TERMINAL_NAME}", host, port)
    args_modify = f"-code {package_code} -weight 15 -status picked_up"
    client = safe_send(client, listener, args_modify, host, port)
    input(f"[SCÉNARIO 2 - Étape {step}/{total_steps}] Terminé. Appuyez sur Entrée pour continuer...")

    # --- Étape 4 : READ après MODIFY ---
    step += 1
    print(f"[SCÉNARIO 2 - Étape {step}/{total_steps}] Lecture après modification...")
    client = safe_send(client, listener, f"READ {TERMINAL_NAME}", host, port)
    client = safe_send(client, listener, f"-code {package_code}", host, port)
    input(f"[SCÉNARIO 2 - Étape {step}/{total_steps}] Terminé. Appuyez sur Entrée pour continuer...")

    # --- Étape 5 : DELETE ---
    step += 1
    print(f"[SCÉNARIO 2 - Étape {step}/{total_steps}] Suppression du colis...")
    client = safe_send(client, listener, f"DELETE {TERMINAL_NAME}", host, port)
    client = safe_send(client, listener, f"-code {package_code}", host, port)
    input(f"[SCÉNARIO 2 - Étape {step}/{total_steps}] Terminé. Appuyez sur Entrée pour continuer...")

    # --- Étape 6 : READ après DELETE ---
    step += 1
    print(f"[SCÉNARIO 2 - Étape {step}/{total_steps}] Lecture après suppression...")
    client = safe_send(client, listener, f"READ {TERMINAL_NAME}", host, port)
    client = safe_send(client, listener, f"-code {package_code}", host, port)
    input(f"[SCÉNARIO 2 - Étape {step}/{total_steps}] Terminé. Fin du scénario 2. Appuyez sur Entrée pour continuer...")

    client.disconnect()


def scenario_3(host=HOST, port=PORT):
    """
    Scénario 3 : Lecture d'un package qui n'existe pas
    """
    listener = ScenarioListener()
    client = SocketClient(host, port, listener)
    client.connect()

    package_code = "PKG_INEXISTANT"
    total_steps = 1
    step = 1

    print(f"[SCÉNARIO 3 - Étape {step}/{total_steps}] Lecture d'un colis inexistant...")
    client = safe_send(client, listener, f"READ {TERMINAL_NAME}", host, port)
    client = safe_send(client, listener, f"-code {package_code}", host, port)
    input(f"[SCÉNARIO 3 - Étape {step}/{total_steps}] Terminé. Fin du scénario 3. Appuyez sur Entrée pour continuer...")

    client.disconnect()


def scenario_4(host=HOST, port=PORT):
    """
    Scénario 4 : Tentative d'ajout d'un package sans informations obligatoires
    """
    listener = ScenarioListener()
    client = SocketClient(host, port, listener)
    client.connect()

    total_steps = 1
    step = 1

    print(f"[SCÉNARIO 4 - Étape {step}/{total_steps}] Tentative d'ajout d'un colis sans code ni spacecode...")
    client = safe_send(client, listener, f"ADD {TERMINAL_NAME}", host, port)
    args_incomplete = "-weight 10 -status in_storage"
    client = safe_send(client, listener, args_incomplete, host, port)
    input(f"[SCÉNARIO 4 - Étape {step}/{total_steps}] Terminé. Fin du scénario 4. Appuyez sur Entrée pour continuer...")

    client.disconnect()

def scenario_5(host=HOST, port=PORT):
    """
    Scénario 5 : Tentative d'ajout d'un package sans source ni destination
    """
    listener = ScenarioListener()
    client = SocketClient(host, port, listener)
    client.connect()

    package_code = f"{PACKAGE_CODE}_S5"
    total_steps = 3
    step = 1

    # --- Étape 1 : ADD ---
    print(f"[SCÉNARIO 5 - Étape {step}/{total_steps}] Ajout du colis sans source ni destination...")
    client = safe_send(client, listener, f"ADD {TERMINAL_NAME}", host, port)
    args_add = f"-code {package_code} -fragile true -refrigerated false -spacecode E403 " \
               f"-weight 10 -status in_storage -estimated_delivery {date(2025, 12, 15)}"
    client = safe_send(client, listener, args_add, host, port)
    input(f"[SCÉNARIO 5 - Étape {step}/{total_steps}] Terminé. Appuyez sur Entrée pour continuer...")

    # --- Étape 2 : READ ---
    step += 1
    print(f"[SCÉNARIO 5 - Étape {step}/{total_steps}] Lecture du colis ajouté (pour vérifier quoi le serveur a accepté)...")
    client = safe_send(client, listener, f"READ {TERMINAL_NAME}", host, port)
    client = safe_send(client, listener, f"-code {package_code}", host, port)
    input(f"[SCÉNARIO 5 - Étape {step}/{total_steps}] Terminé. Appuyez sur Entrée pour continuer...")

    # --- Étape 3 : DELETE ---
    step += 1
    print(f"[SCÉNARIO 5 - Étape {step}/{total_steps}] Suppression du colis...")
    client = safe_send(client, listener, f"DELETE {TERMINAL_NAME}", host, port)
    client = safe_send(client, listener, f"-code {package_code}", host, port)
    input(f"[SCÉNARIO 5 - Étape {step}/{total_steps}] Terminé. Fin du scénario 5. Appuyez sur Entrée pour continuer...")

    client.disconnect()




# ======================
# MAIN CLI
# ======================
def main():
    scenarios = {
        "1": scenario_1,
        "2": scenario_2,
        "3": scenario_3,
        "4": scenario_4,
        "5": scenario_5
    }

    while True:
        print("\n=== MENU SCÉNARIOS ===")
        print("1: Ajout puis suppression d'un colis")
        print("2: Ajout, modification, lecture, suppression")
        print("3: Lire un colis inexistant")
        print("4: Tentative d'ajout sans infos obligatoires")
        print("5: Ajout, puis suppression d'un colis sans source ni destination")
        print("q: Quitter")

        choice = input("Sélectionnez un scénario (1-5) ou q pour quitter: ").strip()
        if choice.lower() == "q":
            print("Au revoir !")
            break
        elif choice in scenarios:
            scenarios[choice](HOST, PORT)
        else:
            print("[ERROR] Choix invalide, réessayez.")


if __name__ == "__main__":
    main()
