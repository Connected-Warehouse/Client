import threading
import time
import ipaddress
from datetime import date

from client.SocketClient import SocketClient
from client.listener.MyListener import MyListener
from client.Message import Message

# ======================
# LISTENER POUR LES SCÉNARIOS
# ======================
class ScenarioListener(MyListener):
    def on_connected(self):
        print("[INFO] Connexion au serveur réussie.")
    def on_disconnected(self):
        print("[INFO] Déconnexion du serveur. Vous reviendrez au menu de départ")

    def on_received(self, message: str):
        treat_message(message.strip())
        print("[RECEIVED]", message.strip())
        

    def on_error(self, error: Exception):
        print(f"[ERROR] {error}")

# ======================
# EXCEPTIONS
# ======================
class ServerDisconnected(Exception):
    """Quand la connection au serveur est perdu"""
    pass

# ======================
# FONCTION UTILE D'ENVOI DE MESSAGE
# ======================
def safe_send(client: SocketClient, listener: ScenarioListener, message: str, host="127.0.0.1", port=8888, timeout=2.0):
    """
    Envoie un message au serveur, reconnecte si nécessaire.
    """
    if client is None or not client.connected:
        print(f"[INFO] Client non connecté, tentative de reconnexion...")
        client = SocketClient(host, port, listener)
        client.connect()
        if not client.connected:
            print("[ERROR] Reconnexion échouée. Retour au départ")
            raise ServerDisconnected

    try:
        print(f"[SENDING] {message}")
        RESPONDED.clear()
        client.send_message(message)
        time.sleep(timeout)#le serveur a 2 seconde pour répondre
        if(not (RESPONDED.is_set())):
            print("[ERROR] Serveur a pris plus de deux seconde à répondre. Fin de la connexion")
            raise ServerDisconnected
    except Exception as e:
        print(f"[ERROR] Échec envoi message : {e}")
        raise ServerDisconnected
    except ServerDisconnected as e:
        print(f"[ERROR] Échec envoi message : {e}")
        raise ServerDisconnected
    return client

def treat_message(message):
    """
    Traite le message pour communiquer une autorisation de passage.
    """
    RESPONDED.set()
    if(message.startswith("ALLOWED")):
        PERMITTED.set()
        #print("Test Réussi allowed")
    elif(message.startswith("ERROR")):
        return
        #print("Test Réussi ERROR") 
    elif(message.startswith("FINISHED")):
        FINISHED.set()
        return
    return
# ======================
# CONSTANTES
# ======================
TERMINAL_NAME = "A001"
PACKAGE_CODE = "PKG777"
HOST = "127.0.0.1"
PORT = 8888
CONNECTED = 0
PERMITTED = threading.Event()
FINISHED = threading.Event()
SHOULD_RESET=0

RESPONDED = threading.Event()

def resetState():
    RESPONDED.clear()
    PERMITTED.clear()
    FINISHED.clear()
# ======================
# SCÉNARIOS
# ======================

def scenario_0(host=HOST, port=PORT):
    """
    Scénario 0 : Action Manuelle, le plus important des scénarios
    """
    port = int(port)
    listener = ScenarioListener()
    client = SocketClient(host, port, listener)
    client.connect()
    #Vérification et indication de connexion effective
    if(not client.connected):
        print(f"[ERROR] Échec de connexion")
        return
    action=input("Choisissez une action à faire parmis ADD, READ, MODIFY, DELETE : ").strip()
    if(not client.connected):
        print(f"[ERROR] Échec de connexion")
        return
    terminal_name=input("Entrez le nom de votre terminal : ").strip()
    try:
        if(action=="READ"):
            read(client,listener,host,port,terminal_name)
        elif(action=="ADD"):
            add(client,listener,host,port,terminal_name)
        elif(action=="MODIFY"):
            modify(client,listener,host,port,terminal_name)
        elif(action=="DELETE"):
            delete(client,listener,host,port,terminal_name)
        else:
            print(f"Erreur: veuillez choisir une action parmis celles proposés.")
    except ServerDisconnected:
        print(f"[ERROR] Connexion au serveur terminé, retour au menu de départ")
        return
    client.disconnect

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

def scenario_6(host=HOST, port=PORT):
    """
    Scénario 6 : Envoi d'une requête énorme pour tester le serveur
    """
    listener = ScenarioListener()
    client = SocketClient(host, port, listener)
    client.connect()

    package_code = f"{PACKAGE_CODE}_LARGE"
    total_steps = 1
    step = 1

    print(f"[SCÉNARIO 6 - Étape {step}/{total_steps}] Envoi d'un colis avec données volumineuses...")

    client = safe_send(client, listener, f"ADD {TERMINAL_NAME}", host, port)

    # Création d'une très grande chaîne pour tester le serveur
    huge_text = "X" * 300  # 300 caractères

    args_add = f"-code {package_code} -fragile true -refrigerated false -spacecode E403 " \
               f"-source {huge_text}@email.com -destination {huge_text}@gmail.com " \
               f"-weight 10 -status in_storage -estimated_delivery {date(2025, 12, 31)} " \
               f"-notes {huge_text}"

    client = safe_send(client, listener, args_add, host, port)

    input(f"[SCÉNARIO 6 - Étape {step}/{total_steps}] Terminé. Appuyez sur Entrée pour continuer...")

    client.disconnect()

# ======================
# ACTION FUNCTIONS
# ======================

def read(client,listener,host,port,terminal_name):
    try:
        print(f"Lecture par le terminal {terminal_name}")
        client = safe_send(client, listener, f"READ {terminal_name}", host, port)
        if(not PERMITTED.is_set()):
            print(f"Accès non autorisé")
            return
        #vérification de la réponse allowed, erreur et retour sinon.
        package_code=input("Veuillez entrer le code du package a lire : ")
        data = {"code": package_code}
        #validation des données
        is_valid, msg = Message.validate_data(data, "READ")
        if not is_valid:
            print(f"Message {msg} non valide, veuillez revoir le format")
            return
        client = safe_send(client, listener, Message.build_param_cmd(data), host, port)
        input(f"Lecture Terminé. Appuyez sur Entrée pour continuer...")
    except ServerDisconnected:
        raise ServerDisconnected
    return

def add(client, listener, host, port, terminal_name):
    try:
        print(f"Ajout d'un colis par le terminal {terminal_name}")
        client = safe_send(client, listener, Message.build_action_cmd("ADD", terminal_name), host, port)
        if(not PERMITTED.is_set()):
            print(f"Accès non autorisé")
            return
        package_info = {
            "code": input("Code colis (PKG+lettres/chiffres) : ").strip(),
            "fragile": input("Fragile (true/false) : ").strip().lower() or "false",
            "refrigerated": input("Réfrigéré (true/false) : ").strip().lower() or "false",
            "spacecode": input("Zone de stockage (ex: E403) : ").strip(),
            "source": input("Email expéditeur : ").strip(),
            "destination": input("Email destinataire : ").strip(),
            "weight": input("Poids (kg) : ").strip(),
            "status": input("Statut (in_storage/picked_up) : ").strip() or "in_storage",
            "estimated_delivery": input("Date de livraison estimée (AAAA-MM-JJ) : ").strip()
        }
        # Validation des données
        is_valid, msg = Message.validate_data(package_info, "ADD")
        if not is_valid:
            print(f"Message {msg} non valide, veuillez revoir le format {msg}")
            return

        # Envoi des données
        client = safe_send(client, listener, Message.build_param_cmd(package_info), host, port)
    except ServerDisconnected:
        raise ServerDisconnected
    input(f"Appuyez sur Entrée pour continuer...")
    return

def modify(client, listener, host, port, terminal_name):

    print(f"Modification d'un colis par le terminal {terminal_name}")
    try:
        client = safe_send(client, listener, Message.build_action_cmd("MODIFY", terminal_name), host, port)
        if(not PERMITTED.is_set()):
            print(f"Accès non autorisé")
            return
        # Collecte des données
        modify_info = {
            "code": input("Code colis : ").strip(),
            "weight": input("Nouveau poids (laisser vide pour ne pas modifier) : ").strip(),
            "status": input("Nouveau statut (laisser vide pour ne pas modifier) : ").strip(),
            "refrigerated": input("Nouvel état réfrigéré (true/false, laisser vide pour ne pas modifier) : ").strip().lower()
        }

        # Filtrage des valeurs vides
        modify_info = {k: v for k, v in modify_info.items() if v.strip()}

        # Validation des données
        is_valid, msg = Message.validate_data(modify_info, "MODIFY")
        if not is_valid:
            print(f" {msg} n'est pas une donnée valide")
            return

        # Envoi des données
        client = safe_send(client, listener, Message.build_param_cmd(modify_info), host, port)
    except ServerDisconnected:
        raise ServerDisconnected
    input("\n Appuyez sur Entrée pour continuer...")
    return

def delete(client,listener,host,port,terminal_name):
    print(f"Suppression par le terminal {terminal_name}")
    try:
        client = safe_send(client, listener, Message.build_action_cmd("DELETE", terminal_name), host, port)
        if(not PERMITTED.is_set()):
            print(f"Accès non autorisé")
            return
        package_code=input("Veuillez entrer le code du package a lire")
        data = {"code": package_code}
        is_valid, msg = Message.validate_data(data, "DELETE")
        if not is_valid:
            print(f"Message {msg} non valide, veuillez revoir le format")
            return
        client = safe_send(client, listener, Message.build_param_cmd(data), host, port)
    except ServerDisconnected:
        raise ServerDisconnected
    input(f"Suppression Terminé. Appuyez sur Entrée pour continuer...")

# ======================
# MAIN CLI
# ======================
def main():
    scenarios = {
        "1": scenario_1,
        "2": scenario_2,
        "3": scenario_3,
        "4": scenario_4,
        "5": scenario_5,
        "6":scenario_6
    }

    while True:
        print("\n=== UTILISATION MANUELLE ===")
        print("0: Scénario manuel (l'utilisateur entre ses valeurs manuellement)")
        print("\n=== MENU SCÉNARIOS AUTOMATISÉS ===")
        print("1: Ajout puis suppression d'un colis")
        print("2: Ajout, modification, lecture, suppression")
        print("3: Lire un colis inexistant")
        print("4: Tentative d'ajout sans infos obligatoires")
        print("5: Ajout, puis suppression d'un colis sans source ni destination")
        print("6: Envoi d'une trop grosse requête")
        print("q: Quitter")

        choice = input("Sélectionnez un scénario (0-6) ou q pour quitter: ").strip()
        if choice.lower() == "q":
            print("Au revoir !")
            break
        elif choice == "0":
            chosen_port=input("Entrez le port par lequel se connecter. Entrez d pour la valeure par défaut : ").strip()
            if(chosen_port=="d"):
                chosen_port=str(PORT)
            if(not chosen_port.isdigit):
                print("[ERROR] Choix de port invalide, réessayez.")
                return
            chosen_host=input("Entrez l'adresse à laquelle se connecter : ").strip()
            try:
                ipaddress.ip_address(chosen_host)
            except ValueError:
                print("[ERROR] Choix d'adresse invalide, réessayez.")
                return
            scenario_0(chosen_host, chosen_port)
        elif choice in scenarios:
            scenarios[choice](HOST, PORT)
        else:
            print("[ERROR] Choix invalide, réessayez.")
        resetState()

if __name__ == "__main__":
    main()
