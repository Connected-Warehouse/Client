# On met ici les protocoles / messages attendus par le serveur pour la communication.
# Les messages ici sont des exemples simples

def get_welcome_message(name: str) -> str:
    return f"Bonjour, je suis {name}"

def get_goodbye_message() -> str:
    return "Au revoir!"
